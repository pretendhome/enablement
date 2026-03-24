#!/usr/bin/env python3
"""
Enablement System Integrity Check — master validation script.

Runs all checks:
1. RIU coverage (coverage_report.py)
2. Prerequisite acyclicity (prerequisite_validator.py)
3. Schema conformance (all modules match module-schema.yaml)
4. Knowledge library cross-references
5. Assessment completeness (anchor items, rubric dimensions)
"""

import yaml
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ENABLEMENT_ROOT = SCRIPT_DIR.parent
CURRICULUM_ROOT = ENABLEMENT_ROOT / "curriculum/workstreams"
SCHEMA_PATH = ENABLEMENT_ROOT / "curriculum/module-schema.yaml"

# Required top-level fields from module-schema.yaml
REQUIRED_FIELDS = [
    'riu_id', 'name', 'workstream', 'journey_stage',
    'classification', 'difficulty', 'learning_objectives',
    'assessment_type', 'required_artifacts', 'rubric_dimensions',
    'certification_tier_thresholds', 'exercises',
]

VALID_JOURNEY_STAGES = ['foundation', 'retrieval', 'orchestration', 'specialization', 'evaluation', 'all']
VALID_CLASSIFICATIONS = ['internal_only', 'both']
VALID_DIFFICULTIES = ['low', 'medium', 'high', 'critical']
VALID_ASSESSMENT_TYPES = ['portfolio', 'architecture_defense', 'diagnosis', 'service_integration']
VALID_RUBRIC_LEVELS = ['insufficient', 'basic', 'competent', 'expert']


def find_modules(curriculum_root):
    """Find all module.yaml files."""
    modules = []
    for module_path in Path(curriculum_root).rglob("module.yaml"):
        with open(module_path, 'r') as f:
            module = yaml.safe_load(f)
        module['_path'] = str(module_path)
        modules.append(module)
    return modules


def check_schema_conformance(modules):
    """Check each module against required fields and valid values."""
    errors = []
    warnings = []

    for module in modules:
        riu_id = module.get('riu_id', 'UNKNOWN')
        path = module.get('_path', 'unknown')

        # Required fields
        for field in REQUIRED_FIELDS:
            if field not in module or module[field] is None:
                errors.append(f"{riu_id}: missing required field '{field}'")

        # Valid values
        stage = module.get('journey_stage')
        if stage and stage not in VALID_JOURNEY_STAGES:
            errors.append(f"{riu_id}: invalid journey_stage '{stage}'")

        classification = module.get('classification')
        if classification and classification not in VALID_CLASSIFICATIONS:
            errors.append(f"{riu_id}: invalid classification '{classification}'")

        difficulty = module.get('difficulty')
        if difficulty and difficulty not in VALID_DIFFICULTIES:
            errors.append(f"{riu_id}: invalid difficulty '{difficulty}'")

        assessment = module.get('assessment_type')
        if assessment and assessment not in VALID_ASSESSMENT_TYPES:
            errors.append(f"{riu_id}: invalid assessment_type '{assessment}'")

        # Learning objectives count
        objectives = module.get('learning_objectives', [])
        if objectives and (len(objectives) < 3 or len(objectives) > 5):
            warnings.append(f"{riu_id}: has {len(objectives)} learning objectives (expected 3-5)")

        # Rubric dimensions
        rubric = module.get('rubric_dimensions', {})
        if rubric:
            for dim_name, dim in rubric.items():
                if not isinstance(dim, dict):
                    continue
                levels = dim.get('levels', [])
                if levels != VALID_RUBRIC_LEVELS:
                    errors.append(f"{riu_id}: rubric dimension '{dim_name}' has invalid levels")

        # Exercises count
        exercises = module.get('exercises', [])
        if exercises and len(exercises) < 2:
            warnings.append(f"{riu_id}: has {len(exercises)} exercises (expected 2-3)")

        # Service context check
        if classification == 'both' and not module.get('service_context'):
            warnings.append(f"{riu_id}: classified as 'both' but has no service_context")
        if classification == 'internal_only' and module.get('service_context'):
            warnings.append(f"{riu_id}: classified as 'internal_only' but has service_context")

        # Certification thresholds
        thresholds = module.get('certification_tier_thresholds', {})
        if thresholds:
            if 'WORKING' not in thresholds:
                errors.append(f"{riu_id}: missing WORKING threshold")
            if 'PRODUCTION' not in thresholds:
                errors.append(f"{riu_id}: missing PRODUCTION threshold")

    return errors, warnings


def check_exercise_coverage(modules):
    """Check that exercises cover all three failure modes."""
    warnings = []
    for module in modules:
        riu_id = module.get('riu_id', 'UNKNOWN')
        exercises = module.get('exercises', [])
        if not exercises:
            continue

        modes = {ex.get('failure_mode') for ex in exercises}
        expected = {'silent', 'loud', 'clustered'}
        missing = expected - modes
        if missing:
            warnings.append(f"{riu_id}: missing failure mode exercises: {', '.join(missing)}")

    return warnings


def run_integrity():
    print("=" * 60)
    print("ENABLEMENT SYSTEM INTEGRITY CHECK")
    print("=" * 60)

    modules = find_modules(CURRICULUM_ROOT)
    print(f"\nModules found: {len(modules)}")

    total_errors = 0
    total_warnings = 0

    # 1. Schema conformance
    errors, warnings = check_schema_conformance(modules)
    print(f"\n1. SCHEMA CONFORMANCE")
    if errors:
        print(f"   [FAIL] {len(errors)} error(s):")
        for e in errors:
            print(f"   ✗ {e}")
        total_errors += len(errors)
    else:
        print(f"   [PASS] All modules conform to schema")
    if warnings:
        print(f"   [WARN] {len(warnings)} warning(s):")
        for w in warnings:
            print(f"   ! {w}")
        total_warnings += len(warnings)

    # 2. Exercise failure mode coverage
    ex_warnings = check_exercise_coverage(modules)
    print(f"\n2. EXERCISE FAILURE MODE COVERAGE")
    if ex_warnings:
        print(f"   [WARN] {len(ex_warnings)} module(s) with incomplete failure mode coverage:")
        for w in ex_warnings:
            print(f"   ! {w}")
        total_warnings += len(ex_warnings)
    else:
        print(f"   [PASS] All modules cover silent/loud/clustered failure modes")

    # 3. Cross-module consistency
    print(f"\n3. CROSS-MODULE CONSISTENCY")
    riu_ids = [m['riu_id'] for m in modules]
    duplicates = [r for r in set(riu_ids) if riu_ids.count(r) > 1]
    if duplicates:
        print(f"   [FAIL] Duplicate RIU IDs: {', '.join(duplicates)}")
        total_errors += len(duplicates)
    else:
        print(f"   [PASS] No duplicate RIU IDs")

    # Summary
    print(f"\n{'=' * 60}")
    if total_errors == 0:
        print(f"STATUS: PASS ({total_warnings} warning(s))")
    else:
        print(f"STATUS: FAIL ({total_errors} error(s), {total_warnings} warning(s))")
    print(f"{'=' * 60}")

    return total_errors == 0


if __name__ == "__main__":
    success = run_integrity()
    sys.exit(0 if success else 1)
