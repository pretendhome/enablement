#!/usr/bin/env python3
"""
Palette Developer Enablement & Certification System — Demo Runner

End-to-end CLI for browsing modules, viewing exercises, running the
evaluation pipeline, inspecting learning journeys, and showing system stats.

Usage:
    python3 demo_runner.py browse [--track TRACK] [--workstream WORKSTREAM] [--stage STAGE]
    python3 demo_runner.py module RIU-XXX
    python3 demo_runner.py exercise RIU-XXX [--exercise N]
    python3 demo_runner.py evaluate SUBMISSION_DIR MODULE_PATH
    python3 demo_runner.py journey TRACK
    python3 demo_runner.py stats
"""

import argparse
import os
import sys
import textwrap
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

# ── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
ENABLEMENT_ROOT = SCRIPT_DIR.parent
CURRICULUM_ROOT = ENABLEMENT_ROOT / "curriculum" / "workstreams"
JOURNEYS_ROOT = ENABLEMENT_ROOT / "curriculum" / "journeys"
CAPSTONES_ROOT = ENABLEMENT_ROOT / "assessment" / "capstones"
AUTOMATED_CHECKS = ENABLEMENT_ROOT / "assessment" / "evaluators" / "automated_checks.py"
AI_RUBRIC_PROMPT = ENABLEMENT_ROOT / "assessment" / "evaluators" / "ai_rubric_evaluator_prompt.md"

# ── Terminal formatting ──────────────────────────────────────────────────────

try:
    TERM_WIDTH = min(os.get_terminal_size().columns, 120)
except (ValueError, OSError):
    TERM_WIDTH = 100

BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[97m"


def supports_color():
    """Check whether the terminal supports ANSI color."""
    if os.environ.get("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    return True


USE_COLOR = supports_color()


def c(code, text):
    """Wrap text in an ANSI color code if color is supported."""
    if USE_COLOR:
        return f"{code}{text}{RESET}"
    return text


def header_box(title, subtitle=None):
    """Print a prominent section header."""
    width = TERM_WIDTH
    border = "=" * width
    lines = [
        "",
        c(CYAN, border),
        c(BOLD + WHITE, f"  {title}"),
    ]
    if subtitle:
        lines.append(c(DIM, f"  {subtitle}"))
    lines.append(c(CYAN, border))
    print("\n".join(lines))


def section(title):
    """Print a section header."""
    print(f"\n{c(BOLD + YELLOW, title)}")
    print(c(DIM, "-" * len(title)))


def kv(key, value, indent=2):
    """Print a key-value pair."""
    pad = " " * indent
    print(f"{pad}{c(BOLD, key + ':')} {value}")


def bullet(text, indent=4, marker="-"):
    """Print a wrapped bullet point."""
    pad = " " * indent
    prefix = f"{pad}{marker} "
    wrapper = textwrap.TextWrapper(
        width=TERM_WIDTH - 2,
        initial_indent=prefix,
        subsequent_indent=" " * len(prefix),
    )
    print(wrapper.fill(text))


def bar_chart(label, count, total, width=30, color=GREEN):
    """Print a simple horizontal bar."""
    pct = count / total if total else 0
    filled = int(pct * width)
    bar = c(color, "#" * filled) + c(DIM, "." * (width - filled))
    print(f"  {label:<28s} [{bar}] {count:>3d}  ({pct:>5.1%})")


def wrap_paragraph(text, indent=4):
    """Print a wrapped paragraph."""
    pad = " " * indent
    wrapper = textwrap.TextWrapper(
        width=TERM_WIDTH - 2,
        initial_indent=pad,
        subsequent_indent=pad,
    )
    print(wrapper.fill(text))


# ── Data loading ─────────────────────────────────────────────────────────────

def load_yaml_file(path):
    """Load a YAML file and return its contents."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def discover_modules():
    """Walk the workstreams tree and load every module.yaml."""
    modules = []
    for module_path in sorted(CURRICULUM_ROOT.rglob("module.yaml")):
        try:
            data = load_yaml_file(module_path)
            data["_path"] = str(module_path)
            data["_workstream_dir"] = module_path.parent.parent.name
            modules.append(data)
        except Exception as e:
            print(f"  [WARN] Could not load {module_path}: {e}", file=sys.stderr)
    return modules


def discover_journeys():
    """Load all journey YAML files."""
    journeys = {}
    for jpath in sorted(JOURNEYS_ROOT.glob("*.yaml")):
        try:
            data = load_yaml_file(jpath)
            track_key = jpath.stem  # e.g., "ai_foundations"
            data["_path"] = str(jpath)
            journeys[track_key] = data
        except Exception as e:
            print(f"  [WARN] Could not load {jpath}: {e}", file=sys.stderr)
    return journeys


def find_module_by_riu(modules, riu_id):
    """Find a module by RIU ID (case-insensitive)."""
    target = riu_id.upper()
    for m in modules:
        if m.get("riu_id", "").upper() == target:
            return m
    return None


def find_capstone(track_key):
    """Find the capstone file for a journey track."""
    capstone_path = CAPSTONES_ROOT / f"{track_key}_capstone.md"
    if capstone_path.is_file():
        return capstone_path.read_text()
    return None


# ── Difficulty / stage display helpers ───────────────────────────────────────

DIFFICULTY_COLORS = {
    "low": GREEN,
    "medium": YELLOW,
    "high": RED,
    "critical": BOLD + RED,
}

STAGE_COLORS = {
    "foundation": GREEN,
    "retrieval": CYAN,
    "orchestration": MAGENTA,
    "specialization": YELLOW,
    "evaluation": RED,
    "governance": BOLD + CYAN,
    "ops": BOLD + YELLOW,
    "all": DIM,
}


def fmt_difficulty(d):
    return c(DIFFICULTY_COLORS.get(d, ""), d)


def fmt_stage(s):
    return c(STAGE_COLORS.get(s, ""), s)


# ── Command: browse ─────────────────────────────────────────────────────────

def cmd_browse(args):
    """List modules with optional filters."""
    modules = discover_modules()
    journeys = discover_journeys()

    # Build a mapping from RIU-ID to journey track names
    riu_to_tracks = {}
    for track_key, jdata in journeys.items():
        track_name = jdata.get("track", track_key)
        for entry in jdata.get("module_sequence", []):
            rid = entry.get("riu_id", "")
            riu_to_tracks.setdefault(rid, []).append(track_name)

    # Apply filters
    filtered = modules
    if args.track:
        track_key = args.track.lower().replace(" ", "_")
        j = journeys.get(track_key)
        if j:
            track_rius = {e["riu_id"] for e in j.get("module_sequence", [])}
            filtered = [m for m in filtered if m.get("riu_id") in track_rius]
        else:
            # Try matching by track name substring
            for tk, jdata in journeys.items():
                if args.track.lower() in jdata.get("track", "").lower():
                    track_rius = {e["riu_id"] for e in jdata.get("module_sequence", [])}
                    filtered = [m for m in filtered if m.get("riu_id") in track_rius]
                    break
            else:
                print(f"  Track '{args.track}' not found. Available tracks:")
                for tk, jdata in journeys.items():
                    print(f"    {tk} ({jdata.get('track', tk)})")
                return

    if args.workstream:
        ws_lower = args.workstream.lower().replace("_", " ").replace("-", " ")
        filtered = [
            m for m in filtered
            if ws_lower in m.get("workstream", "").lower().replace("&", "and").replace("-", " ")
            or ws_lower in m.get("_workstream_dir", "").lower().replace("-", " ")
        ]

    if args.stage:
        filtered = [m for m in filtered if m.get("journey_stage", "").lower() == args.stage.lower()]

    if not filtered:
        print("  No modules match the given filters.")
        return

    # Sort by RIU-ID numerically
    def sort_key(m):
        rid = m.get("riu_id", "RIU-000")
        try:
            return int(rid.split("-")[1])
        except (IndexError, ValueError):
            return 0

    filtered.sort(key=sort_key)

    # Header
    header_box(
        "Palette Enablement — Module Browser",
        f"{len(filtered)} modules" + (f" (of {len(modules)} total)" if len(filtered) != len(modules) else ""),
    )

    # Table header
    hdr = f"  {'RIU':<10s} {'Name':<42s} {'Diff':<10s} {'Stage':<16s} {'Assessment':<22s}"
    print(f"\n{c(BOLD, hdr)}")
    print(f"  {'-'*10} {'-'*42} {'-'*10} {'-'*16} {'-'*22}")

    for m in filtered:
        riu = m.get("riu_id", "?")
        name = m.get("name", "?")
        if len(name) > 40:
            name = name[:37] + "..."
        diff = m.get("difficulty", "?")
        stage = m.get("journey_stage", "?")
        atype = m.get("assessment_type", "?")

        print(
            f"  {c(BOLD, riu):<21s} {name:<42s} {fmt_difficulty(diff):<21s} {fmt_stage(stage):<27s} {atype:<22s}"
        )

    # Footer legend
    print(f"\n{c(DIM, '  Tracks: ' + ', '.join(sorted(journeys.keys())))}")
    ws_names = sorted({m.get('workstream', '?') for m in modules})
    print(c(DIM, f"  Workstreams: {', '.join(ws_names)}"))
    print(c(DIM, f"  Stages: foundation, retrieval, orchestration, specialization, evaluation, all"))
    print()


# ── Command: module ──────────────────────────────────────────────────────────

def cmd_module(args):
    """Display the full details of a single module."""
    modules = discover_modules()
    m = find_module_by_riu(modules, args.riu_id)
    if not m:
        print(f"  Module '{args.riu_id}' not found.")
        return

    header_box(
        f"{m['riu_id']} — {m.get('name', '?')}",
        f"{m.get('workstream', '?')}  |  {m.get('journey_stage', '?')}  |  {m.get('difficulty', '?')}  |  {m.get('classification', '?')}",
    )

    # Learning objectives
    section("Learning Objectives")
    for i, obj in enumerate(m.get("learning_objectives", []), 1):
        bullet(obj, marker=f"{i}.")

    # Prerequisites
    section("Prerequisites")
    prereqs = m.get("prerequisites", {})
    required = prereqs.get("required", []) or []
    recommended = prereqs.get("recommended", []) or []
    if required:
        for r in required:
            bullet(f"{r} {c(RED, '(required)')}")
    if recommended:
        for r in recommended:
            bullet(f"{r} {c(DIM, '(recommended)')}")
    if not required and not recommended:
        print(f"    {c(DIM, 'None')}")

    # Knowledge library entries
    kl = m.get("knowledge_library_entries", {})
    if kl:
        section("Knowledge Library References")
        primary = kl.get("primary", []) or []
        supporting = kl.get("supporting", []) or []
        if primary:
            print(f"    {c(BOLD, 'Primary:')}  {', '.join(primary)}")
        if supporting:
            print(f"    {c(DIM, 'Supporting:')} {', '.join(supporting)}")

    # Service context
    svc = m.get("service_context")
    if svc:
        section("Service Context")
        for s in svc.get("candidate_services", []):
            bullet(s)
        recipes = svc.get("integration_recipes", [])
        if recipes:
            print(f"\n    {c(DIM, 'Integration recipes:')}")
            for r in recipes:
                bullet(r, indent=6)

    # Duration
    section("Estimated Duration")
    dur = m.get("estimated_duration", {})
    kv("Learning", dur.get("learning", "?"))
    kv("Assessment", dur.get("assessment", "?"))

    # Exercises
    exercises = m.get("exercises", [])
    section(f"Exercises ({len(exercises)})")
    for i, ex in enumerate(exercises, 1):
        fm = ex.get("failure_mode", "?")
        fm_color = {"silent": RED, "loud": YELLOW, "clustered": MAGENTA}.get(fm, DIM)
        print(f"\n    {c(BOLD, f'Exercise {i}')}  [{ex.get('id', '?')}]  failure mode: {c(fm_color, fm)}")
        wrap_paragraph(ex.get("scenario", ""), indent=6)

    # Required artifacts
    section("Required Artifacts")
    for art in m.get("required_artifacts", []):
        parts = art.split(" — ", 1)
        if len(parts) == 2:
            bullet(f"{c(BOLD, parts[0])} — {parts[1]}")
        else:
            bullet(art)

    # Rubric dimensions
    section("Rubric Dimensions")
    dims = m.get("rubric_dimensions", {})
    for dname, dinfo in dims.items():
        desc = dinfo.get("description", "")
        levels = ", ".join(dinfo.get("levels", []))
        print(f"    {c(BOLD, dname)}")
        wrap_paragraph(desc, indent=6)
        print(f"      Levels: {c(DIM, levels)}")

    # Certification thresholds
    section("Certification Thresholds")
    thresholds = m.get("certification_tier_thresholds", {})
    kv("WORKING", c(GREEN, thresholds.get("WORKING", "?")))
    kv("PRODUCTION", c(CYAN, thresholds.get("PRODUCTION", "?")))

    source_path = m.get("_path", "?")
    print(f"\n{c(DIM, f'  Source: {source_path}')} ")
    print()


# ── Command: exercise ────────────────────────────────────────────────────────

def cmd_exercise(args):
    """Present a single exercise in learner-facing format."""
    modules = discover_modules()
    m = find_module_by_riu(modules, args.riu_id)
    if not m:
        print(f"  Module '{args.riu_id}' not found.")
        return

    exercises = m.get("exercises", [])
    if not exercises:
        print(f"  Module {args.riu_id} has no exercises.")
        return

    idx = (args.exercise or 1) - 1
    if idx < 0 or idx >= len(exercises):
        print(f"  Exercise {args.exercise} not found. Module has {len(exercises)} exercise(s).")
        return

    ex = exercises[idx]
    total = len(exercises)

    header_box(
        f"{m['riu_id']} — {m.get('name', '?')}",
        f"Exercise {idx + 1} of {total}",
    )

    # Scenario
    section("Scenario")
    print()
    wrap_paragraph(ex.get("scenario", ""), indent=4)

    # What you need to produce
    section("What You Need to Produce")
    print()
    fm = ex.get("failure_mode", "?")
    fm_labels = {
        "silent": "This scenario tests a failure that happens silently — no one notices until it's too late.",
        "loud": "This scenario tests a failure that's visible and urgent — everyone notices at once.",
        "clustered": "This scenario tests multiple interacting failures — complexity compounds.",
    }
    wrap_paragraph(
        fm_labels.get(fm, f"Failure mode: {fm}"),
        indent=4,
    )

    print()
    wrap_paragraph(ex.get("expected_output", ""), indent=4)

    # Artifacts to submit
    section("Artifacts to Submit")
    for art in m.get("required_artifacts", []):
        parts = art.split(" — ", 1)
        if len(parts) == 2:
            bullet(f"{c(BOLD, parts[0])} — {parts[1]}")
        else:
            bullet(art)

    # Navigation hint
    if total > 1:
        others = [str(i + 1) for i in range(total) if i != idx]
        print(f"\n{c(DIM, f'  Other exercises: {', '.join(others)}')}")
        print(c(DIM, f"  Run: python3 demo_runner.py exercise {m['riu_id']} --exercise N"))
    print()


# ── Command: evaluate ────────────────────────────────────────────────────────

def cmd_evaluate(args):
    """Run the full 3-layer evaluation pipeline."""
    submission_dir = Path(args.submission_dir).resolve()
    module_path = Path(args.module_path).resolve()

    if not submission_dir.is_dir():
        print(f"  Submission directory not found: {submission_dir}")
        sys.exit(1)
    if not module_path.is_file():
        print(f"  Module file not found: {module_path}")
        sys.exit(1)

    module = load_yaml_file(module_path)
    riu_id = module.get("riu_id", "UNKNOWN")
    mod_name = module.get("name", "?")

    header_box(
        f"Evaluation Pipeline — {riu_id}",
        f"{mod_name}",
    )

    # ── Layer 1: Automated Checks ────────────────────────────────────────

    section("Layer 1: Automated Checks")
    print()

    # Import and run the existing automated_checks module
    import importlib.util
    spec = importlib.util.spec_from_file_location("automated_checks", str(AUTOMATED_CHECKS))
    ac = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ac)

    layer1_pass = ac.run_automated_checks(str(submission_dir), str(module_path))
    print()

    if not layer1_pass:
        print(c(RED, "  Layer 1 FAILED. Fix the issues above before proceeding to Layer 2."))
        print(c(DIM, "  Layer 2 and Layer 3 skipped."))
        print()
        return

    print(c(GREEN, "  Layer 1 PASSED. Proceeding to Layer 2 preparation."))

    # ── Layer 2: AI Rubric Evaluator Prompt Assembly ─────────────────────

    section("Layer 2: AI Rubric Evaluator — Prompt Assembly")
    print()

    # Read the AI rubric evaluator system prompt template
    rubric_template = AI_RUBRIC_PROMPT.read_text()

    # Read submission artifacts
    artifact_contents = {}
    for fpath in sorted(submission_dir.rglob("*")):
        if fpath.is_file():
            rel = str(fpath.relative_to(submission_dir))
            try:
                content = fpath.read_text()
                artifact_contents[rel] = content
            except UnicodeDecodeError:
                artifact_contents[rel] = f"[Binary file — {fpath.stat().st_size} bytes]"

    # Build the rubric section
    dims = module.get("rubric_dimensions", {})
    rubric_yaml = yaml.dump({"rubric_dimensions": dims}, default_flow_style=False, sort_keys=False)

    thresholds = module.get("certification_tier_thresholds", {})
    thresholds_yaml = yaml.dump(
        {"certification_tier_thresholds": thresholds}, default_flow_style=False, sort_keys=False
    )

    # Assemble the complete prompt
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    submission_id = f"SUB-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M')}"

    assembled_prompt_parts = [
        rubric_template,
        "",
        "---",
        "",
        "# Evaluation Request",
        "",
        f"**Module:** {riu_id} — {mod_name}",
        f"**Submission ID:** {submission_id}",
        f"**Timestamp:** {timestamp}",
        "",
        "## Module Rubric",
        "",
        "```yaml",
        rubric_yaml.strip(),
        "```",
        "",
        "## Certification Thresholds",
        "",
        "```yaml",
        thresholds_yaml.strip(),
        "```",
        "",
        "## Submitted Artifacts",
        "",
    ]

    for artifact_name, content in artifact_contents.items():
        assembled_prompt_parts.extend([
            f"### `{artifact_name}`",
            "",
            "```",
            content.strip(),
            "```",
            "",
        ])

    # Include calibration exemplars if available
    calibration_path = ENABLEMENT_ROOT / "assessment" / "item-banks" / riu_id / "calibration_exemplars.md"
    if calibration_path.exists():
        exemplar_text = calibration_path.read_text().strip()
        assembled_prompt_parts.extend([
            "## Calibration Exemplars",
            "",
            "Use these exemplars to calibrate your scoring. Each level shows what a submission",
            "at that quality looks like for this module's rubric dimensions.",
            "",
            exemplar_text,
            "",
        ])

    assembled_prompt_parts.extend([
        "## Instructions",
        "",
        "Evaluate each rubric dimension using the calibration rules in the system prompt.",
        "Output your evaluation in the YAML format specified above.",
        f"Set module to \"{riu_id}\" and submission_id to \"{submission_id}\".",
        "",
    ])

    assembled_prompt = "\n".join(assembled_prompt_parts)

    # Write the prompt to a file
    prompt_output_path = submission_dir / f"layer2_evaluation_prompt_{riu_id.lower()}.md"
    prompt_output_path.write_text(assembled_prompt)

    cal_status = "included" if calibration_path.exists() else "not available"
    print(f"  Assembled evaluation prompt: {c(BOLD, str(artifact_contents.keys().__len__()))} artifact(s) included")
    print(f"  Calibration exemplars: {c(GREEN if calibration_path.exists() else YELLOW, cal_status)}")
    print(f"  Prompt length: {len(assembled_prompt):,} characters")
    print(f"  Written to: {c(CYAN, str(prompt_output_path))}")
    print()
    print(c(DIM, "  To run Layer 2: paste the contents of the file above into Claude or another LLM."))
    print(c(DIM, "  The prompt includes the system instructions, rubric, and all submission artifacts."))

    # ── Layer 2 prompt preview ───────────────────────────────────────────

    section("Layer 2: Prompt Preview (first 40 lines)")
    print()
    preview_lines = assembled_prompt.split("\n")[:40]
    for line in preview_lines:
        print(f"  {c(DIM, '|')} {line}")
    if len(assembled_prompt.split("\n")) > 40:
        remaining = len(assembled_prompt.split("\n")) - 40
        print(f"  {c(DIM, f'| ... ({remaining} more lines)')}")

    # ── Layer 3: Human Review Summary ────────────────────────────────────

    section("Layer 3: Human Review — Escalation Summary")
    print()

    print(f"  {c(BOLD, 'Escalation triggers for this module:')}")
    print()
    bullet("Any rubric dimension scored with LOW confidence by the AI evaluator")
    bullet("Overall result is borderline (exactly at WORKING threshold)")
    bullet("2+ dimensions at adjacent levels with medium confidence")
    bullet("Any PRODUCTION-tier evaluation (requires human sign-off)")

    thresholds = module.get("certification_tier_thresholds", {})
    print()
    print(f"  {c(BOLD, 'Thresholds the human reviewer checks:')}")
    kv("WORKING", thresholds.get("WORKING", "?"), indent=4)
    kv("PRODUCTION", thresholds.get("PRODUCTION", "?"), indent=4)

    # Module-specific review areas
    print()
    print(f"  {c(BOLD, 'What the human reviewer focuses on:')}")
    for dname, dinfo in dims.items():
        bullet(f"{dname}: {dinfo.get('description', '')}")

    print()
    print(c(DIM, "  Human review is mandatory for PRODUCTION certification."))
    print(c(DIM, "  10% of WORKING submissions are sampled for calibration."))
    print()

    # ── Threshold Engine Demo ─────────────────────────────────────────────

    section("Threshold Engine — Live Evaluation Demo")
    print()

    try:
        evaluators_dir = str(ENABLEMENT_ROOT / "assessment" / "evaluators")
        if evaluators_dir not in sys.path:
            sys.path.insert(0, evaluators_dir)
        from threshold_engine import check_certification

        dim_names = list(dims.keys())

        # Scenario 1: All competent
        scores_competent = {d: "competent" for d in dim_names}
        result1 = check_certification(str(module_path), scores_competent)

        # Scenario 2: Mix of expert and competent
        scores_mixed = {d: "expert" for d in dim_names}
        for d in dim_names[len(dim_names)//2:]:
            scores_mixed[d] = "competent"
        result2 = check_certification(str(module_path), scores_mixed)

        # Scenario 3: One basic
        scores_weak = {d: "competent" for d in dim_names}
        scores_weak[dim_names[0]] = "basic"
        result3 = check_certification(str(module_path), scores_weak)

        scenarios = [
            ("All competent", scores_competent, result1),
            ("Mix expert + competent", scores_mixed, result2),
            (f"One basic ({dim_names[0]})", scores_weak, result3),
        ]

        for label, scores, result in scenarios:
            w = result["working"]
            p = result["production"]
            w_icon = c(GREEN, "PASS") if w["passed"] else c(RED, "FAIL")
            p_icon = c(GREEN, "PASS") if p["passed"] else c(RED, "FAIL")
            print(f"  {c(BOLD, label)}: scores = {{{', '.join(f'{k}: {v}' for k, v in scores.items())}}}")
            print(f"    WORKING:    {w_icon}  {c(DIM, w['detail'])}")
            print(f"    PRODUCTION: {p_icon}  {c(DIM, p['detail'])}")
            if w.get("mandatory_failures"):
                print(f"    {c(RED, 'Mandatory failures: ' + ', '.join(w['mandatory_failures']))}")
            print()

    except ImportError:
        print(c(YELLOW, "  Threshold engine not available — skipping live evaluation demo."))
        print()


# ── Command: journey ─────────────────────────────────────────────────────────

def cmd_journey(args):
    """Display the full learning journey for a track."""
    journeys = discover_journeys()
    track_key = args.track.lower().replace(" ", "_")

    jdata = journeys.get(track_key)
    if not jdata:
        # Try fuzzy match
        for tk, jd in journeys.items():
            if track_key in tk or track_key in jd.get("track", "").lower().replace(" ", "_"):
                jdata = jd
                track_key = tk
                break
        if not jdata:
            print(f"  Journey '{args.track}' not found. Available tracks:")
            for tk, jd in journeys.items():
                print(f"    {tk} — {jd.get('track', tk)}")
            return

    modules = discover_modules()
    mod_lookup = {m["riu_id"]: m for m in modules}

    track_name = jdata.get("track", track_key)
    stage = jdata.get("stage_focus", "?")

    header_box(
        f"Learning Journey — {track_name}",
        f"Focus: {stage}  |  Duration: {jdata.get('estimated_total_duration', '?')}",
    )

    # Entry requirements
    section("Entry Requirements")
    entry = jdata.get("entry_requirements", {})
    kv("Placement", entry.get("placement_stage", "?"))
    print()
    prereqs = entry.get("prerequisites", [])
    if prereqs:
        print(f"    {c(BOLD, 'Prerequisites:')}")
        for p in prereqs:
            bullet(p, indent=6)
    baseline = entry.get("expected_baseline", [])
    if baseline:
        print(f"    {c(BOLD, 'Expected baseline:')}")
        for b in baseline:
            bullet(b, indent=6)

    # Module sequence
    seq = jdata.get("module_sequence", [])
    section(f"Module Sequence ({len(seq)} modules)")
    print()

    total_learning_hours = 0
    total_assess_hours = 0

    for i, entry in enumerate(seq, 1):
        rid = entry.get("riu_id", "?")
        rationale = entry.get("rationale", "")
        m = mod_lookup.get(rid)

        if m:
            name = m.get("name", "?")
            diff = m.get("difficulty", "?")
            dur = m.get("estimated_duration", {})
            learning = dur.get("learning", "?")
            assess = dur.get("assessment", "?")
            ws = m.get("workstream", "?")

            # Try to parse hours for totals
            for time_str, accumulator in [(learning, "learn"), (assess, "assess")]:
                try:
                    parts = time_str.replace(" hours", "").replace(" hour", "").split("-")
                    avg = sum(float(p) for p in parts) / len(parts)
                    if accumulator == "learn":
                        total_learning_hours += avg
                    else:
                        total_assess_hours += avg
                except (ValueError, AttributeError):
                    pass

            print(
                f"  {c(BOLD, f'{i:>2}.')} {c(CYAN, rid):<20s} {name}"
            )
            print(
                f"      {c(DIM, f'{ws}  |  {diff}  |  learn: {learning}  |  assess: {assess}')}"
            )
        else:
            print(f"  {c(BOLD, f'{i:>2}.')} {c(CYAN, rid):<20s} {c(RED, '[module not found]')}")

        if rationale:
            wrap_paragraph(rationale, indent=6)
        print()

    # Duration summary
    section("Duration Estimate")
    kv("Learning", f"~{total_learning_hours:.0f} hours")
    kv("Assessment", f"~{total_assess_hours:.0f} hours")
    kv("Total (computed)", f"~{total_learning_hours + total_assess_hours:.0f} hours")
    kv("Total (stated)", jdata.get("estimated_total_duration", "?"))

    # Ordering notes
    notes = jdata.get("ordering_notes", [])
    if notes:
        section("Design Notes")
        for note in notes:
            bullet(note)

    # Capstone
    capstone_text = find_capstone(track_key)
    if capstone_text:
        section("Capstone Project")
        print()
        # Extract key sections from capstone markdown
        lines = capstone_text.split("\n")
        in_section = None
        shown_sections = {"Title", "Summary", "Target Duration", "Required Deliverables", "Scenario", "Thresholds"}
        for line in lines:
            if line.startswith("## "):
                sec_name = line[3:].strip()
                in_section = sec_name if sec_name in shown_sections else None
                if in_section:
                    print(f"    {c(BOLD, sec_name)}")
            elif in_section:
                stripped = line.strip()
                if stripped:
                    if stripped.startswith("- "):
                        bullet(stripped[2:], indent=6)
                    else:
                        wrap_paragraph(stripped, indent=6)
    else:
        cap_ref = jdata.get("capstone_reference", "")
        if cap_ref:
            print(f"\n  {c(DIM, f'Capstone reference: {cap_ref}')}")

    print()


# ── Command: stats ───────────────────────────────────────────────────────────

def cmd_stats(args):
    """Show system-level statistics."""
    modules = discover_modules()
    journeys = discover_journeys()

    header_box(
        "Palette Developer Enablement & Certification System",
        f"System Statistics — {datetime.now().strftime('%Y-%m-%d')}",
    )

    # Overview
    section("Overview")
    kv("Total modules", str(len(modules)))
    kv("Learning journeys", str(len(journeys)))
    kv("Capstone projects", str(len(list(CAPSTONES_ROOT.glob("*.md")))) if CAPSTONES_ROOT.is_dir() else "?")

    total_learning = 0
    total_assess = 0
    for m in modules:
        dur = m.get("estimated_duration", {})
        for time_str, which in [(dur.get("learning", ""), "learn"), (dur.get("assessment", ""), "assess")]:
            try:
                parts = time_str.replace(" hours", "").replace(" hour", "").split("-")
                avg = sum(float(p) for p in parts) / len(parts)
                if which == "learn":
                    total_learning += avg
                else:
                    total_assess += avg
            except (ValueError, AttributeError):
                pass

    kv("Total learning hours", f"~{total_learning:.0f}")
    kv("Total assessment hours", f"~{total_assess:.0f}")
    kv("Total curriculum hours", f"~{total_learning + total_assess:.0f}")

    # Workstream distribution
    ws_counts = Counter(m.get("workstream", "Unknown") for m in modules)
    section("Workstream Distribution")
    for ws, count in ws_counts.most_common():
        bar_chart(ws, count, len(modules))

    # Journey stage distribution
    stage_counts = Counter(m.get("journey_stage", "Unknown") for m in modules)
    section("Journey Stage Distribution")
    stage_order = ["foundation", "retrieval", "orchestration", "specialization", "evaluation", "all"]
    for stage in stage_order:
        count = stage_counts.get(stage, 0)
        if count > 0:
            color = STAGE_COLORS.get(stage, GREEN)
            bar_chart(stage, count, len(modules), color=color)
    # Any stages not in the expected list
    for stage, count in stage_counts.most_common():
        if stage not in stage_order and count > 0:
            bar_chart(stage, count, len(modules))

    # Difficulty distribution
    diff_counts = Counter(m.get("difficulty", "Unknown") for m in modules)
    section("Difficulty Distribution")
    for diff in ["low", "medium", "high", "critical"]:
        count = diff_counts.get(diff, 0)
        if count > 0:
            color = DIFFICULTY_COLORS.get(diff, GREEN)
            bar_chart(diff, count, len(modules), color=color)

    # Assessment type distribution
    assess_counts = Counter(m.get("assessment_type", "Unknown") for m in modules)
    section("Assessment Type Distribution")
    for atype, count in assess_counts.most_common():
        bar_chart(atype, count, len(modules), color=CYAN)

    # Classification distribution
    class_counts = Counter(m.get("classification", "Unknown") for m in modules)
    section("Classification (Internal vs Service-Integrated)")
    for cls, count in class_counts.most_common():
        svc_count = sum(
            1 for m in modules
            if m.get("classification") == cls and m.get("service_context") is not None
        )
        bar_chart(f"{cls}", count, len(modules), color=MAGENTA)
        if svc_count:
            print(f"  {'':28s}  ({svc_count} with service context)")

    # Knowledge library utilization
    kl_referenced = set()
    for m in modules:
        kl = m.get("knowledge_library_entries", {})
        if kl:
            for lib_id in kl.get("primary", []) or []:
                kl_referenced.add(lib_id)
            for lib_id in kl.get("supporting", []) or []:
                kl_referenced.add(lib_id)

    section("Knowledge Library Utilization")
    kv("Entries referenced", str(len(kl_referenced)))
    kv("Target utilization", ">80% of 163 entries")

    # Learning journeys
    section("Learning Journeys")
    for tk, jd in sorted(journeys.items()):
        track_name = jd.get("track", tk)
        seq_len = len(jd.get("module_sequence", []))
        duration = jd.get("estimated_total_duration", "?")
        stage = jd.get("stage_focus", "?")
        print(
            f"    {c(BOLD, track_name):<38s} {seq_len:>2d} modules  |  {duration:<14s}  |  focus: {fmt_stage(stage)}"
        )

    # Assessment pipeline summary
    section("3-Layer Assessment Pipeline")
    print()
    print(f"    {c(BOLD + GREEN, 'Layer 1')}  Automated Checks")
    print(f"    {c(DIM, '        Artifacts present, code parses, sources cited, YAML valid')}")
    print()
    print(f"    {c(BOLD + CYAN, 'Layer 2')}  AI Rubric Evaluation")
    print(f"    {c(DIM, '        Per-dimension scoring (insufficient/basic/competent/expert)')}")
    print(f"    {c(DIM, '        Calibrated against exemplars, confidence-scored')}")
    print()
    print(f"    {c(BOLD + MAGENTA, 'Layer 3')}  Human Review")
    print(f"    {c(DIM, '        10% calibration sample + all PRODUCTION submissions')}")
    print(f"    {c(DIM, '        Triggered by low confidence, borderline results, or escalation')}")

    # Certification tiers
    section("Certification Tiers")
    print()
    print(f"    {c(BOLD + GREEN, 'WORKING')}      Developer can apply the competency in guided contexts")
    print(f"    {c(BOLD + CYAN, 'PRODUCTION')}   Developer can apply the competency independently in production")

    print()
    print(c(DIM, f"  Report generated from: {CURRICULUM_ROOT}"))
    print()


# ── CLI entrypoint ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="demo_runner",
        description="Palette Developer Enablement & Certification System — Demo Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              python3 demo_runner.py browse
              python3 demo_runner.py browse --track ai_foundations
              python3 demo_runner.py browse --workstream "quality"
              python3 demo_runner.py browse --stage foundation
              python3 demo_runner.py module RIU-002
              python3 demo_runner.py exercise RIU-002 --exercise 1
              python3 demo_runner.py evaluate ./my-submission ./curriculum/workstreams/clarify-and-bound/RIU-002/module.yaml
              python3 demo_runner.py journey ai_foundations
              python3 demo_runner.py stats
        """),
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # browse
    p_browse = subparsers.add_parser("browse", help="List available modules with filters")
    p_browse.add_argument("--track", "-t", help="Filter by learning journey track (e.g., ai_foundations)")
    p_browse.add_argument("--workstream", "-w", help="Filter by workstream (e.g., quality)")
    p_browse.add_argument("--stage", "-s", help="Filter by journey stage (e.g., foundation)")

    # module
    p_module = subparsers.add_parser("module", help="Display full module details")
    p_module.add_argument("riu_id", help="Module RIU ID (e.g., RIU-002)")

    # exercise
    p_exercise = subparsers.add_parser("exercise", help="Present a single exercise for a learner")
    p_exercise.add_argument("riu_id", help="Module RIU ID (e.g., RIU-002)")
    p_exercise.add_argument("--exercise", "-e", type=int, default=1, help="Exercise number (default: 1)")

    # evaluate
    p_evaluate = subparsers.add_parser("evaluate", help="Run the full evaluation pipeline")
    p_evaluate.add_argument("submission_dir", help="Path to the submission directory")
    p_evaluate.add_argument("module_path", help="Path to the module.yaml file")

    # journey
    p_journey = subparsers.add_parser("journey", help="Display learning journey for a track")
    p_journey.add_argument("track", help="Track name (e.g., ai_foundations, rag_engineer)")

    # stats
    subparsers.add_parser("stats", help="Show system-level statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    commands = {
        "browse": cmd_browse,
        "module": cmd_module,
        "exercise": cmd_exercise,
        "evaluate": cmd_evaluate,
        "journey": cmd_journey,
        "stats": cmd_stats,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
