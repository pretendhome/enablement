#!/usr/bin/env python3
"""
Coverage Report — verifies enablement system coverage against Palette taxonomy.

Checks:
1. RIU coverage: how many of 117 RIUs have modules?
2. KL utilization: what % of 163 knowledge library entries are referenced?
3. Workstream balance: module distribution across workstreams
4. Classification coverage: internal_only vs both
5. Journey stage distribution
"""

import yaml
import os
import sys
from pathlib import Path
from collections import Counter

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).parent
ENABLEMENT_ROOT = SCRIPT_DIR.parent
PALETTE_ROOT = ENABLEMENT_ROOT.parent / "palette"

TAXONOMY_PATH = PALETTE_ROOT / "taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml"
KNOWLEDGE_PATH = PALETTE_ROOT / "knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml"
CLASSIFICATION_PATH = PALETTE_ROOT / "buy-vs-build/service-routing/v1.0/riu_classification_v1.0.yaml"
CURRICULUM_ROOT = ENABLEMENT_ROOT / "curriculum/workstreams"


def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def find_modules(curriculum_root):
    """Find all module.yaml files in the curriculum tree."""
    modules = []
    for module_path in Path(curriculum_root).rglob("module.yaml"):
        with open(module_path, 'r') as f:
            module = yaml.safe_load(f)
        module['_path'] = str(module_path)
        modules.append(module)
    return modules


def extract_riu_ids(taxonomy):
    """Extract all RIU IDs from taxonomy."""
    rius = []
    for ws in taxonomy.get('workstreams_detail', []):
        for riu in ws.get('rius', []):
            rius.append(riu['riu_id'])
    # Also check flat list
    if not rius:
        for riu in taxonomy.get('rius', []):
            rius.append(riu['riu_id'])
    return rius


def extract_kl_ids(knowledge_lib):
    """Extract all LIB IDs from knowledge library."""
    return [q['id'] for q in knowledge_lib.get('library_questions', [])]


def run_coverage_report():
    print("=" * 60)
    print("ENABLEMENT SYSTEM COVERAGE REPORT")
    print("=" * 60)

    # Load data
    if not TAXONOMY_PATH.exists():
        print(f"\n[ERROR] Taxonomy not found at {TAXONOMY_PATH}")
        sys.exit(1)

    taxonomy = load_yaml(TAXONOMY_PATH)
    modules = find_modules(CURRICULUM_ROOT)

    # Count total RIUs from taxonomy
    all_rius = set()
    for riu in taxonomy.get('rius', []):
        all_rius.add(riu.get('riu_id'))
    total_rius = len(all_rius) if all_rius else 117  # fallback

    # Module coverage
    module_rius = {m['riu_id'] for m in modules}
    covered = module_rius & all_rius if all_rius else module_rius
    missing = all_rius - module_rius if all_rius else set()

    print(f"\n1. RIU COVERAGE")
    print(f"   Total RIUs in taxonomy: {total_rius}")
    print(f"   Modules created:        {len(modules)}")
    print(f"   Coverage:               {len(modules)}/{total_rius} ({100*len(modules)/total_rius:.1f}%)")
    if missing and len(missing) <= 20:
        print(f"   Missing: {', '.join(sorted(missing))}")
    elif missing:
        print(f"   Missing: {len(missing)} RIUs (run with --verbose to list)")

    # KL utilization
    kl_referenced = set()
    for m in modules:
        kl = m.get('knowledge_library_entries', {})
        if kl:
            for lib_id in kl.get('primary', []) or []:
                kl_referenced.add(lib_id)
            for lib_id in kl.get('supporting', []) or []:
                kl_referenced.add(lib_id)

    if KNOWLEDGE_PATH.exists():
        kl_data = load_yaml(KNOWLEDGE_PATH)
        all_kl_ids = set(extract_kl_ids(kl_data))
        total_kl = len(all_kl_ids)
    else:
        total_kl = 163

    print(f"\n2. KNOWLEDGE LIBRARY UTILIZATION")
    print(f"   Total KL entries:       {total_kl}")
    print(f"   Referenced by modules:  {len(kl_referenced)}")
    print(f"   Utilization:            {100*len(kl_referenced)/total_kl:.1f}%")
    print(f"   Target:                 >80%")

    # Workstream distribution
    ws_counts = Counter(m.get('workstream', 'Unknown') for m in modules)
    print(f"\n3. WORKSTREAM DISTRIBUTION")
    for ws, count in ws_counts.most_common():
        print(f"   {ws}: {count}")

    # Journey stage distribution
    stage_counts = Counter(m.get('journey_stage', 'Unknown') for m in modules)
    print(f"\n4. JOURNEY STAGE DISTRIBUTION")
    for stage in ['foundation', 'retrieval', 'orchestration', 'specialization', 'evaluation', 'all']:
        count = stage_counts.get(stage, 0)
        if count > 0:
            print(f"   {stage}: {count}")

    # Classification coverage
    class_counts = Counter(m.get('classification', 'Unknown') for m in modules)
    print(f"\n5. CLASSIFICATION COVERAGE")
    for cls, count in class_counts.most_common():
        has_service = sum(1 for m in modules
                         if m.get('classification') == cls
                         and m.get('service_context') is not None)
        print(f"   {cls}: {count} modules ({has_service} with service context)")

    # Difficulty distribution
    diff_counts = Counter(m.get('difficulty', 'Unknown') for m in modules)
    print(f"\n6. DIFFICULTY DISTRIBUTION")
    for diff in ['low', 'medium', 'high', 'critical']:
        count = diff_counts.get(diff, 0)
        if count > 0:
            print(f"   {diff}: {count}")

    # Assessment type distribution
    assess_counts = Counter(m.get('assessment_type', 'Unknown') for m in modules)
    print(f"\n7. ASSESSMENT TYPE DISTRIBUTION")
    for atype, count in assess_counts.most_common():
        print(f"   {atype}: {count}")

    print(f"\n{'=' * 60}")
    status = "PASS" if len(modules) == total_rius else "IN PROGRESS"
    print(f"STATUS: {status}")
    print(f"{'=' * 60}")

    return len(modules) == total_rius


if __name__ == "__main__":
    success = run_coverage_report()
    sys.exit(0 if success else 1)
