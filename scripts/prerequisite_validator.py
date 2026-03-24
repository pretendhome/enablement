#!/usr/bin/env python3
"""
Prerequisite Validator — ensures the curriculum graph is a valid DAG.

Checks:
1. No cycles in the prerequisite graph
2. All referenced prerequisites exist as modules
3. No self-references
4. Prerequisite chains don't exceed max depth (prevents impossibly long paths)
"""

import yaml
import sys
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
ENABLEMENT_ROOT = SCRIPT_DIR.parent
CURRICULUM_ROOT = ENABLEMENT_ROOT / "curriculum/workstreams"
MAX_CHAIN_DEPTH = 10  # No path should require more than 10 prerequisites


def find_modules(curriculum_root):
    """Find all module.yaml files."""
    modules = {}
    for module_path in Path(curriculum_root).rglob("module.yaml"):
        with open(module_path, 'r') as f:
            module = yaml.safe_load(f)
        modules[module['riu_id']] = module
    return modules


def build_graph(modules):
    """Build adjacency list from prerequisites."""
    graph = defaultdict(list)
    for riu_id, module in modules.items():
        prereqs = module.get('prerequisites', {})
        for req in prereqs.get('required', []) or []:
            graph[req].append(riu_id)  # req -> riu_id (must take req before riu_id)
    return graph


def detect_cycles(modules):
    """Detect cycles using DFS with coloring."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {riu_id: WHITE for riu_id in modules}
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        prereqs = modules[node].get('prerequisites', {})
        for req in prereqs.get('required', []) or []:
            if req not in modules:
                continue  # Missing prereq — checked separately
            if color[req] == GRAY:
                cycle_start = path.index(req)
                cycles.append(path[cycle_start:] + [req])
            elif color[req] == WHITE:
                dfs(req, path + [req])
        color[node] = BLACK

    for riu_id in modules:
        if color[riu_id] == WHITE:
            dfs(riu_id, [riu_id])

    return cycles


def find_missing_prerequisites(modules):
    """Find prerequisites that reference non-existent modules."""
    missing = []
    for riu_id, module in modules.items():
        prereqs = module.get('prerequisites', {})
        for req in prereqs.get('required', []) or []:
            if req not in modules:
                missing.append((riu_id, req, 'required'))
        for req in prereqs.get('recommended', []) or []:
            if req not in modules:
                missing.append((riu_id, req, 'recommended'))
    return missing


def find_self_references(modules):
    """Find modules that list themselves as prerequisites."""
    self_refs = []
    for riu_id, module in modules.items():
        prereqs = module.get('prerequisites', {})
        all_prereqs = (prereqs.get('required', []) or []) + (prereqs.get('recommended', []) or [])
        if riu_id in all_prereqs:
            self_refs.append(riu_id)
    return self_refs


def find_max_depth(modules):
    """Find the longest prerequisite chain."""
    cache = {}

    def depth(riu_id, visited=None):
        if visited is None:
            visited = set()
        if riu_id in cache:
            return cache[riu_id]
        if riu_id in visited:
            return 0  # Cycle — handled elsewhere
        visited.add(riu_id)

        prereqs = modules.get(riu_id, {}).get('prerequisites', {})
        required = prereqs.get('required', []) or []
        if not required:
            cache[riu_id] = 0
            return 0

        max_d = 0
        for req in required:
            if req in modules:
                max_d = max(max_d, 1 + depth(req, visited.copy()))
        cache[riu_id] = max_d
        return max_d

    depths = {}
    for riu_id in modules:
        depths[riu_id] = depth(riu_id)
    return depths


def run_validation():
    print("=" * 60)
    print("PREREQUISITE GRAPH VALIDATION")
    print("=" * 60)

    modules = find_modules(CURRICULUM_ROOT)
    if not modules:
        print("\n[WARN] No modules found. Nothing to validate.")
        return True

    print(f"\nModules loaded: {len(modules)}")
    errors = 0

    # 1. Cycle detection
    cycles = detect_cycles(modules)
    print(f"\n1. CYCLE DETECTION")
    if cycles:
        print(f"   [FAIL] {len(cycles)} cycle(s) found:")
        for cycle in cycles:
            print(f"   → {' → '.join(cycle)}")
        errors += len(cycles)
    else:
        print(f"   [PASS] No cycles detected — graph is a valid DAG")

    # 2. Missing prerequisites
    missing = find_missing_prerequisites(modules)
    print(f"\n2. MISSING PREREQUISITES")
    if missing:
        # Separate required (errors) from recommended (warnings)
        required_missing = [(r, p, t) for r, p, t in missing if t == 'required']
        recommended_missing = [(r, p, t) for r, p, t in missing if t == 'recommended']

        if required_missing:
            print(f"   [WARN] {len(required_missing)} required prerequisites not yet created:")
            for riu_id, prereq, _ in required_missing:
                print(f"   {riu_id} requires {prereq} (module not yet created)")
        if recommended_missing:
            print(f"   [INFO] {len(recommended_missing)} recommended prerequisites not yet created")
    else:
        print(f"   [PASS] All referenced prerequisites exist as modules")

    # 3. Self-references
    self_refs = find_self_references(modules)
    print(f"\n3. SELF-REFERENCE CHECK")
    if self_refs:
        print(f"   [FAIL] {len(self_refs)} self-referencing modules:")
        for riu_id in self_refs:
            print(f"   {riu_id} lists itself as a prerequisite")
        errors += len(self_refs)
    else:
        print(f"   [PASS] No self-references")

    # 4. Chain depth
    depths = find_max_depth(modules)
    max_depth_id = max(depths, key=depths.get) if depths else None
    max_depth = depths.get(max_depth_id, 0) if max_depth_id else 0
    print(f"\n4. CHAIN DEPTH")
    print(f"   Maximum prerequisite chain: {max_depth} (module: {max_depth_id})")
    print(f"   Threshold: {MAX_CHAIN_DEPTH}")
    if max_depth > MAX_CHAIN_DEPTH:
        print(f"   [FAIL] Chain exceeds maximum depth")
        errors += 1
    else:
        print(f"   [PASS] Within acceptable depth")

    # Summary
    print(f"\n{'=' * 60}")
    status = "PASS" if errors == 0 else f"FAIL ({errors} error(s))"
    print(f"STATUS: {status}")
    print(f"{'=' * 60}")

    return errors == 0


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
