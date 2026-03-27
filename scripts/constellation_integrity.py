#!/usr/bin/env python3
"""
Constellation Integrity Engine

Validates the enablement content engine's learning graph:
  1. Reachability — every published path reachable from a foundation node
  2. Completeness — per-constellation % of nodes published
  3. Routing integrity — no dead links in What's Next sections
  4. Acyclicity — routing graph has no cycles
  5. Progression — difficulty doesn't regress along constellation arcs

Usage:
    python3 constellation_integrity.py
    python3 constellation_integrity.py --json-out report.json
"""

import argparse
import json
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# --- Paths ---
SCRIPT_DIR = Path(__file__).parent
ENABLEMENT_ROOT = SCRIPT_DIR.parent
FDE_ROOT = ENABLEMENT_ROOT.parent
CONTENT_ENGINE = ENABLEMENT_ROOT / "agentic-enablement-system/content-engine"
REGISTRY_PATH = CONTENT_ENGINE / "constellations.yaml"
PATHS_DIR = ENABLEMENT_ROOT / "paths"
SPECS_DIR = CONTENT_ENGINE / "specs"
TAXONOMY_PATH = FDE_ROOT / "palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml"
KL_PATH = FDE_ROOT / "palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml"
CURRICULUM_ROOT = ENABLEMENT_ROOT / "curriculum/workstreams"

DIFFICULTY_ORD = {"low": 1, "medium": 2, "high": 3, "critical": 4}

# --- Phase 1: Load sources ---

def load_registry():
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)

def load_published_paths():
    """Return dict of riu_id -> {path, metadata, whats_next_rius, sections}."""
    paths = {}
    if not PATHS_DIR.exists():
        return paths
    for p in sorted(PATHS_DIR.glob("RIU-*.md")):
        text = p.read_text()
        riu_match = re.search(r'RIU-(\d+)', p.name)
        if not riu_match:
            continue
        riu_id = f"RIU-{riu_match.group(1)}"

        # Extract What's Next RIU references
        whats_next = []
        wn_section = re.search(r'(?:#{2,3}\s*🔗\s*WHAT.S NEXT|#{2,3}\s*WHAT.S NEXT)(.*?)(?=\n#{2,3}\s|\n---|\Z)', text, re.DOTALL | re.IGNORECASE)
        if wn_section:
            wn_text = wn_section.group(1)
            # Check for structured routing comment first: <!-- routing-targets: RIU-022(coming-soon), ... -->
            routing_comment = re.search(r'<!--\s*routing-targets:\s*(.+?)\s*-->', wn_text)
            if routing_comment:
                for m in re.finditer(r'RIU-(\d+)', routing_comment.group(1)):
                    whats_next.append(f"RIU-{m.group(1)}")
            else:
                # Fall back to inline RIU references
                for m in re.finditer(r'RIU-(\d+)', wn_text):
                    whats_next.append(f"RIU-{m.group(1)}")

        # Check for coming-soon markers
        coming_soon_rius = set()
        if wn_section:
            wn_text = wn_section.group(1)
            # Check structured routing comment for status
            routing_comment = re.search(r'<!--\s*routing-targets:\s*(.+?)\s*-->', wn_text)
            if routing_comment:
                for m in re.finditer(r'(RIU-\d+)\(coming-soon\)', routing_comment.group(1)):
                    coming_soon_rius.add(m.group(1))
            # Also check inline prose
            for line in wn_text.split('\n'):
                if re.search(r'coming\s+soon', line, re.IGNORECASE):
                    for m in re.finditer(r'RIU-(\d+)', line):
                        coming_soon_rius.add(f"RIU-{m.group(1)}")

        # Check for unfilled template variables
        unfilled = re.findall(r'\{\{[^}]+\}\}', text)

        # Check for system IDs above START HERE / COPY EVERYTHING BELOW
        # Use the actual marker line, not the instruction that references it
        start_marker = re.search(r'^(?:##\s*▶\s*START HERE|▶\s*COPY EVERYTHING BELOW)', text, re.MULTILINE)
        learner_preamble = text[:start_marker.start()] if start_marker else ""
        leaked_ids = re.findall(r'\bRIU-\d+\b|\bLIB-\d+\b', learner_preamble)
        # Filter: metadata comment lines (HTML comments) are OK
        visible_leaked = [lid for lid in leaked_ids if lid not in _extract_html_comments(learner_preamble)]

        # Check required sections
        required_markers = [
            ("onramp", r'hands-on exercise|copy the text below'),
            ("how_to_use", r'How to use'),
            ("start_here", r'START HERE|COPY EVERYTHING BELOW'),
            ("quick_start", r'⚡.*QUICK START'),
            ("applied", r'🔨.*APPLIED'),
            ("production", r'🏗️.*PRODUCTION'),
            ("after_build", r'AFTER YOU BUILD'),
            ("whats_next", r'WHAT.S NEXT'),
        ]
        missing_sections = [name for name, pat in required_markers if not re.search(pat, text, re.IGNORECASE)]

        # Extract KL references from footer
        kl_refs = re.findall(r'LIB-\d+', text)
        riu_refs = re.findall(r'RIU-\d+', text)

        paths[riu_id] = {
            "file": str(p.relative_to(FDE_ROOT)),
            "whats_next_rius": list(dict.fromkeys(whats_next)),  # dedupe, preserve order
            "coming_soon_rius": coming_soon_rius,
            "unfilled_vars": unfilled,
            "leaked_ids": visible_leaked,
            "missing_sections": missing_sections,
            "kl_refs": list(set(kl_refs)),
            "riu_refs": list(set(riu_refs)),
        }
    return paths

def _extract_html_comments(text):
    """Return all IDs inside HTML comments."""
    comments = re.findall(r'<!--.*?-->', text, re.DOTALL)
    ids = []
    for c in comments:
        ids.extend(re.findall(r'\bRIU-\d+\b|\bLIB-\d+\b', c))
    return set(ids)

def load_specs():
    """Return dict of spec_name -> parsed yaml."""
    specs = {}
    if not SPECS_DIR.exists():
        return specs
    for p in sorted(SPECS_DIR.glob("VIDEO_SPEC_*.yaml")):
        with open(p) as f:
            specs[p.stem] = yaml.safe_load(f)
    return specs

def load_taxonomy_rius():
    with open(TAXONOMY_PATH) as f:
        tax = yaml.safe_load(f)
    return {r['riu_id'] for r in tax.get('rius', [])}

def load_kl_ids():
    with open(KL_PATH) as f:
        kl = yaml.safe_load(f)
    ids = set()
    for section in ['library_questions', 'gap_additions', 'context_specific_questions']:
        for entry in kl.get(section, []):
            if 'id' in entry:
                ids.add(entry['id'])
    return ids

def load_difficulty_map():
    """RIU -> difficulty from curriculum modules."""
    diff = {}
    for p in CURRICULUM_ROOT.rglob("module.yaml"):
        with open(p) as f:
            m = yaml.safe_load(f)
        if m and 'riu_id' in m and 'difficulty' in m:
            diff[m['riu_id']] = m['difficulty']
    return diff

# --- Phase 2: Build graph & resolve statuses ---

def build_graph(registry, published_paths):
    """Build constellation graph with resolved statuses."""
    constellations = []
    all_published_rius = set(published_paths.keys())
    all_registry_rius = set()

    for c in registry.get('constellations', []):
        nodes = []
        for node in c.get('nodes', []):
            riu = node.get('riu')
            declared_status = node.get('status', 'unmapped')
            path_file = node.get('path_file')

            # Resolve actual status
            if riu and riu in all_published_rius:
                actual_status = 'published'
            elif path_file and Path(FDE_ROOT / path_file).exists():
                actual_status = 'published'
            else:
                actual_status = declared_status

            # Detect drift
            drift = None
            if declared_status == 'published' and actual_status != 'published':
                drift = f"Registry says published but path file not found"
            elif declared_status != 'published' and actual_status == 'published':
                drift = f"Registry says {declared_status} but path exists"

            if riu:
                all_registry_rius.add(riu)

            nodes.append({
                "position": node.get('position'),
                "topic": node.get('topic'),
                "riu": riu,
                "declared_status": declared_status,
                "actual_status": actual_status,
                "drift": drift,
            })
        constellations.append({
            "name": c['name'],
            "arc": c.get('arc', ''),
            "nodes": nodes,
        })

    # Find orphan paths (published but not in any constellation)
    orphans = all_published_rius - all_registry_rius

    return constellations, orphans

# --- Phase 3: Compute 5 health metrics ---

def check_reachability(constellations):
    """Every published path should be reachable from a foundation node (position 1)."""
    issues = []
    for c in constellations:
        published = [n for n in c['nodes'] if n['actual_status'] == 'published']
        if not published:
            continue
        foundation = c['nodes'][0] if c['nodes'] else None
        if foundation and foundation['actual_status'] != 'published':
            for p in published:
                if p['position'] != 1:
                    issues.append(f"{c['name']}: {p['riu']} (pos {p['position']}) is published but foundation node (pos 1) is not")
    return "pass" if not issues else "fail", issues

def check_completeness(constellations):
    """Per-constellation completeness."""
    results = []
    for c in constellations:
        total = len(c['nodes'])
        published = sum(1 for n in c['nodes'] if n['actual_status'] == 'published')
        planned = sum(1 for n in c['nodes'] if n['actual_status'] == 'planned')
        unmapped = sum(1 for n in c['nodes'] if n['actual_status'] == 'unmapped')
        pct = (published / total * 100) if total else 0
        results.append({
            "constellation": c['name'],
            "total": total,
            "published": published,
            "planned": planned,
            "unmapped": unmapped,
            "percent_published": round(pct, 1),
            "display_ready": pct >= 66.0,
        })
    return results

def check_routing_integrity(published_paths, constellations):
    """Every What's Next RIU must be published, coming-soon, or in registry as planned."""
    all_registry_rius = set()
    for c in constellations:
        for n in c['nodes']:
            if n['riu']:
                all_registry_rius.add(n['riu'])

    all_published = set(published_paths.keys())
    dead_links = []

    for riu, pdata in published_paths.items():
        for target_riu in pdata['whats_next_rius']:
            if target_riu in all_published:
                continue  # live link
            if target_riu in pdata['coming_soon_rius']:
                continue  # marked coming soon
            if target_riu in all_registry_rius:
                dead_links.append(f"{riu} → {target_riu} (in registry as planned, but not marked 'coming soon' in path)")
            else:
                dead_links.append(f"{riu} → {target_riu} (not published, not in registry, not marked coming soon)")

    return "pass" if not dead_links else "fail", dead_links

def check_acyclicity(published_paths):
    """Check routing graph for cycles using DFS."""
    # Build adjacency list from What's Next
    graph = defaultdict(list)
    for riu, pdata in published_paths.items():
        for target in pdata['whats_next_rius']:
            if target in published_paths:  # only check edges between published paths
                graph[riu].append(target)

    visited = set()
    in_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        in_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in in_stack:
                cycles.append(f"Cycle: {' → '.join(path + [neighbor])}")
                return
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor])
        in_stack.remove(node)

    for node in published_paths:
        if node not in visited:
            dfs(node, [node])

    return "pass" if not cycles else "fail", cycles

def check_progression(constellations, difficulty_map):
    """Difficulty should not regress along constellation sequence."""
    issues = []
    for c in constellations:
        prev_diff = None
        prev_riu = None
        for node in sorted(c['nodes'], key=lambda n: n['position']):
            riu = node.get('riu')
            if not riu or riu not in difficulty_map:
                prev_diff = None
                prev_riu = None
                continue
            curr_diff = DIFFICULTY_ORD.get(difficulty_map[riu])
            if curr_diff is None:
                prev_diff = None
                prev_riu = None
                continue
            if prev_diff is not None and curr_diff < prev_diff:
                issues.append(
                    f"{c['name']}: {riu} (pos {node['position']}, {difficulty_map[riu]}) "
                    f"regresses from {prev_riu} ({difficulty_map.get(prev_riu, '?')})"
                )
            prev_diff = curr_diff
            prev_riu = riu
    return "pass" if not issues else "fail", issues

# --- Phase 4: Supporting checks ---

def check_spec_path_sync(specs, published_paths):
    """Every spec should have a path, every path should have a spec."""
    issues = []
    spec_rius = set()
    for name, spec in specs.items():
        riu = spec.get('classification', {}).get('riu', '')
        if riu:
            spec_rius.add(riu)
            if riu not in published_paths:
                issues.append(f"Spec {name} references {riu} but no published path exists")

    for riu in published_paths:
        if riu not in spec_rius:
            issues.append(f"Published path {riu} has no corresponding video spec")

    return issues

def check_unfilled_vars(published_paths):
    issues = []
    for riu, pdata in published_paths.items():
        if pdata['unfilled_vars']:
            issues.append(f"{riu}: unfilled template variables: {pdata['unfilled_vars'][:5]}")
    return issues

def check_leaked_ids(published_paths):
    issues = []
    for riu, pdata in published_paths.items():
        if pdata['leaked_ids']:
            issues.append(f"{riu}: system IDs visible above START HERE: {pdata['leaked_ids'][:5]}")
    return issues

def check_missing_sections(published_paths):
    issues = []
    for riu, pdata in published_paths.items():
        if pdata['missing_sections']:
            issues.append(f"{riu}: missing sections: {pdata['missing_sections']}")
    return issues

def check_crossrefs(published_paths, valid_rius, valid_kl_ids):
    issues = []
    for riu, pdata in published_paths.items():
        for ref in pdata['riu_refs']:
            if ref not in valid_rius:
                issues.append(f"{riu}: references {ref} which doesn't exist in taxonomy")
        for ref in pdata['kl_refs']:
            if ref not in valid_kl_ids:
                issues.append(f"{riu}: references {ref} which doesn't exist in knowledge library")
    return issues

def check_drift(constellations):
    issues = []
    for c in constellations:
        for n in c['nodes']:
            if n['drift']:
                issues.append(f"{c['name']} pos {n['position']} ({n['riu']}): {n['drift']}")
    return issues

# --- Phase 5: Render ---

def render_human(constellations, orphans, completeness, reachability, routing, acyclicity, progression, supporting, published_paths):
    print("Constellation Integrity Report")
    print("=" * 40)
    print()

    for c, comp in zip(constellations, completeness):
        name = c['name']
        print(f"  {name}")
        nodes_str = ", ".join(
            f"{n['riu'] or '?'}({'✅' if n['actual_status'] == 'published' else '⬜' if n['actual_status'] == 'planned' else '·'})"
            for n in c['nodes']
        )
        print(f"    Nodes: {nodes_str}")
        display = "✅" if comp['display_ready'] else "⚠️  (below 66% — hide map)"
        print(f"    Completeness: {comp['percent_published']}% ({comp['published']}/{comp['total']} published) {display}")

    print()
    print(f"  Published paths: {len(published_paths)}")
    print(f"  Orphan paths (not in any constellation): {len(orphans)}")
    if orphans:
        for o in orphans:
            print(f"    - {o}")
    print()

    # Metrics
    metrics = [
        ("Reachability", reachability),
        ("Routing integrity", routing),
        ("Acyclicity", acyclicity),
        ("Progression", progression),
    ]
    for name, (status, issues) in metrics:
        icon = "✅" if status == "pass" else "❌"
        print(f"  {icon} {name}: {status.upper()}")
        for issue in issues:
            print(f"      - {issue}")

    # Supporting
    print()
    labels = [
        ("Spec-path sync", supporting['spec_path']),
        ("Unfilled variables", supporting['unfilled']),
        ("Leaked system IDs", supporting['leaked']),
        ("Missing sections", supporting['sections']),
        ("Cross-references", supporting['crossrefs']),
        ("Status drift", supporting['drift']),
    ]
    for name, issues in labels:
        icon = "✅" if not issues else ("⚠️ " if len(issues) <= 2 else "❌")
        print(f"  {icon} {name}: {len(issues)} issue(s)")
        for issue in issues:
            print(f"      - {issue}")

    # Verdict
    print()
    all_metric_statuses = [s for s, _ in [reachability, routing, acyclicity, progression]]
    fail_count = sum(1 for s in all_metric_statuses if s == "fail")
    total_issues = sum(len(v) for v in supporting.values())
    if fail_count == 0 and total_issues == 0:
        print("  VERDICT: ALL GREEN ✅")
    elif fail_count == 0:
        print(f"  VERDICT: METRICS PASS, {total_issues} supporting issue(s) ⚠️")
    else:
        print(f"  VERDICT: {fail_count} METRIC FAILURE(S), {total_issues} supporting issue(s) ❌")

    return fail_count > 0

def render_json(constellations, orphans, completeness, reachability, routing, acyclicity, progression, supporting, published_paths, output_path):
    report = {
        "status": "fail" if any(s == "fail" for s, _ in [reachability, routing, acyclicity, progression]) else "pass",
        "summary": {
            "published_paths": len(published_paths),
            "orphans": list(orphans),
            "constellations_defined": len(constellations),
        },
        "constellations": [
            {
                "name": c['name'],
                "completeness": comp,
                "nodes": c['nodes'],
            }
            for c, comp in zip(constellations, completeness)
        ],
        "metrics": {
            "reachability": {"status": reachability[0], "issues": reachability[1]},
            "routing_integrity": {"status": routing[0], "issues": routing[1]},
            "acyclicity": {"status": acyclicity[0], "issues": acyclicity[1]},
            "progression": {"status": progression[0], "issues": progression[1]},
        },
        "supporting": {k: v for k, v in supporting.items()},
    }
    Path(output_path).write_text(json.dumps(report, indent=2))
    print(f"\n  JSON report written to {output_path}")

# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Constellation Integrity Engine")
    parser.add_argument("--json-out", help="Write JSON report to this path")
    args = parser.parse_args()

    # Phase 1: Load
    registry = load_registry()
    published_paths = load_published_paths()
    specs = load_specs()
    valid_rius = load_taxonomy_rius()
    valid_kl_ids = load_kl_ids()
    difficulty_map = load_difficulty_map()

    # Phase 2: Build graph
    constellations, orphans = build_graph(registry, published_paths)

    # Phase 3: Health metrics
    reachability = check_reachability(constellations)
    completeness = check_completeness(constellations)
    routing = check_routing_integrity(published_paths, constellations)
    acyclicity = check_acyclicity(published_paths)
    progression = check_progression(constellations, difficulty_map)

    # Phase 4: Supporting checks
    supporting = {
        "spec_path": check_spec_path_sync(specs, published_paths),
        "unfilled": check_unfilled_vars(published_paths),
        "leaked": check_leaked_ids(published_paths),
        "sections": check_missing_sections(published_paths),
        "crossrefs": check_crossrefs(published_paths, valid_rius, valid_kl_ids),
        "drift": check_drift(constellations),
    }

    # Phase 5: Render
    has_failures = render_human(constellations, orphans, completeness, reachability, routing, acyclicity, progression, supporting, published_paths)

    if args.json_out:
        render_json(constellations, orphans, completeness, reachability, routing, acyclicity, progression, supporting, published_paths, args.json_out)

    sys.exit(1 if has_failures else 0)

if __name__ == "__main__":
    main()
