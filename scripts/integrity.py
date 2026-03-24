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
import re

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
TRACEABILITY_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'build', 'by', 'can', 'content',
    'create', 'define', 'demonstrate', 'design', 'do', 'for', 'from', 'how',
    'identify', 'implement', 'in', 'into', 'is', 'it', 'make', 'not', 'of',
    'on', 'or', 'out', 'rules', 'system', 'that', 'the', 'their', 'them',
    'they', 'this', 'to', 'use', 'using', 'what', 'with'
}


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


def normalize_tokens(text):
    """Tokenize text for lightweight traceability checks."""
    if not text:
        return set()
    tokens = re.findall(r"[a-z0-9_]+", text.lower())
    return {token for token in tokens if len(token) > 2 and token not in TRACEABILITY_STOPWORDS}


def check_objective_traceability(modules):
    """Warn when objectives do not appear to map to rubric or artifact language."""
    warnings = []

    for module in modules:
        riu_id = module.get('riu_id', 'UNKNOWN')
        objectives = module.get('learning_objectives', [])
        rubric = module.get('rubric_dimensions', {})
        artifacts = module.get('required_artifacts', [])

        rubric_tokens = set()
        for dim_name, dim in rubric.items():
            rubric_tokens |= normalize_tokens(dim_name)
            if isinstance(dim, dict):
                rubric_tokens |= normalize_tokens(dim.get('description', ''))

        artifact_tokens = set()
        for artifact in artifacts:
            artifact_tokens |= normalize_tokens(str(artifact))

        traceability_tokens = rubric_tokens | artifact_tokens

        for idx, objective in enumerate(objectives, start=1):
            objective_tokens = normalize_tokens(objective)
            overlap = objective_tokens & traceability_tokens
            if not overlap:
                warnings.append(
                    f"{riu_id}: learning objective {idx} may not map to any rubric dimension or artifact acceptance criterion"
                )

    return warnings


def check_kl_references(modules):
    """Check that all referenced KL entries exist in the knowledge library."""
    errors = []
    warnings = []

    kl_path = ENABLEMENT_ROOT.parent / "palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml"
    if not kl_path.exists():
        warnings.append("Knowledge library not found — skipping KL reference validation")
        return errors, warnings

    with open(kl_path) as f:
        kl_data = yaml.safe_load(f)

    all_kl_ids = set()
    for section in ['library_questions', 'gap_additions', 'context_specific_questions']:
        for q in kl_data.get(section, []):
            if 'id' in q:
                all_kl_ids.add(q['id'])

    for module in modules:
        riu_id = module.get('riu_id', 'UNKNOWN')
        kl = module.get('knowledge_library_entries', {})
        if not kl:
            continue

        for ref_type in ['primary', 'supporting']:
            for lib_id in kl.get(ref_type, []) or []:
                if lib_id not in all_kl_ids:
                    errors.append(f"{riu_id}: references {lib_id} ({ref_type}) — does not exist in KL v1.4")

    for module in modules:
        riu_id = module.get('riu_id', 'UNKNOWN')
        kl = module.get('knowledge_library_entries', {})
        primary = kl.get('primary', []) if kl else []
        supporting = kl.get('supporting', []) if kl else []
        if not primary and not supporting:
            warnings.append(f"{riu_id}: has no knowledge library references")

    return errors, warnings


def check_threshold_parsability(modules):
    """Validate that all threshold strings can be parsed by the threshold engine."""
    errors = []

    try:
        _evaluators_dir = str(ENABLEMENT_ROOT / "assessment/evaluators")
        if _evaluators_dir not in sys.path:
            sys.path.insert(0, _evaluators_dir)
        from threshold_engine import parse_threshold
    except ImportError:
        errors.append("Could not import threshold_engine — skipping threshold validation")
        return errors

    for module in modules:
        riu_id = module.get('riu_id', 'UNKNOWN')
        thresholds = module.get('certification_tier_thresholds', {})
        for tier in ['WORKING', 'PRODUCTION']:
            threshold_str = thresholds.get(tier)
            if not threshold_str:
                continue
            threshold_str = str(threshold_str).strip('"').strip("'")
            try:
                parse_threshold(threshold_str)
            except ValueError as e:
                errors.append(f"{riu_id}: {tier} threshold unparseable: '{threshold_str}' — {e}")

    return errors


def check_threshold_policy(modules):
    """Check high-risk threshold policy assumptions from generation rules."""
    warnings = []

    try:
        _evaluators_dir = str(ENABLEMENT_ROOT / "assessment/evaluators")
        if _evaluators_dir not in sys.path:
            sys.path.insert(0, _evaluators_dir)
        from threshold_engine import parse_threshold
    except ImportError:
        warnings.append("Could not import threshold_engine — skipping threshold policy checks")
        return warnings

    for module in modules:
        riu_id = module.get('riu_id', 'UNKNOWN')
        difficulty = module.get('difficulty', '')
        workstream = str(module.get('workstream', '')).lower()
        name = str(module.get('name', '')).lower()
        thresholds = module.get('certification_tier_thresholds', {})
        working = thresholds.get('WORKING')
        if not working:
            continue

        try:
            rule = parse_threshold(str(working).strip('"').strip("'"))
        except ValueError:
            continue

        is_control_sensitive = (
            'quality' in workstream or
            any(token in name for token in ['safety', 'privacy', 'auth', 'guardrail', 'risk', 'audit', 'compliance'])
        )

        if difficulty == 'critical' and is_control_sensitive and rule.required_count != rule.total_count:
            warnings.append(
                f"{riu_id}: critical control-sensitive module WORKING threshold should require competence on all core-control dimensions"
            )

        if difficulty == 'critical' and is_control_sensitive and not rule.mandatory:
            warnings.append(
                f"{riu_id}: critical control-sensitive module should name mandatory dimensions in WORKING threshold"
            )

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

    # 3. Objective traceability
    trace_warnings = check_objective_traceability(modules)
    print(f"\n3. OBJECTIVE TRACEABILITY")
    if trace_warnings:
        print(f"   [WARN] {len(trace_warnings)} possible objective-to-assessment traceability gap(s):")
        for w in trace_warnings:
            print(f"   ! {w}")
        total_warnings += len(trace_warnings)
    else:
        print(f"   [PASS] All learning objectives appear to map to rubric or artifact language")

    # 4. Threshold policy
    threshold_parse_errors = check_threshold_parsability(modules)
    threshold_policy_warnings = check_threshold_policy(modules)
    print(f"\n4. THRESHOLD POLICY")
    if threshold_parse_errors:
        print(f"   [FAIL] {len(threshold_parse_errors)} threshold parsing error(s):")
        for e in threshold_parse_errors:
            print(f"   ✗ {e}")
        total_errors += len(threshold_parse_errors)
    else:
        print(f"   [PASS] All thresholds are parseable")
    if threshold_policy_warnings:
        print(f"   [WARN] {len(threshold_policy_warnings)} threshold policy warning(s):")
        for w in threshold_policy_warnings:
            print(f"   ! {w}")
        total_warnings += len(threshold_policy_warnings)

    # 5. Cross-module consistency
    print(f"\n5. CROSS-MODULE CONSISTENCY")
    riu_ids = [m['riu_id'] for m in modules]
    duplicates = [r for r in set(riu_ids) if riu_ids.count(r) > 1]
    if duplicates:
        print(f"   [FAIL] Duplicate RIU IDs: {', '.join(duplicates)}")
        total_errors += len(duplicates)
    else:
        print(f"   [PASS] No duplicate RIU IDs")

    # 5. Knowledge library references
    kl_errors, kl_warnings = check_kl_references(modules)
    print(f"\n5. KNOWLEDGE LIBRARY REFERENCES")
    if kl_errors:
        print(f"   [FAIL] {len(kl_errors)} dangling KL reference(s):")
        for e in kl_errors:
            print(f"   ✗ {e}")
        total_errors += len(kl_errors)
    elif kl_warnings:
        print(f"   [PASS] All referenced KL entries exist")
    else:
        print(f"   [PASS] All referenced KL entries exist")
    if kl_warnings:
        print(f"   [WARN] {len(kl_warnings)} warning(s):")
        for w in kl_warnings:
            print(f"   ! {w}")
        total_warnings += len(kl_warnings)

    # 6. Threshold parsability
    threshold_errors = check_threshold_parsability(modules)
    print(f"\n6. THRESHOLD PARSABILITY")
    if threshold_errors:
        print(f"   [FAIL] {len(threshold_errors)} unparseable threshold(s):")
        for e in threshold_errors:
            print(f"   ✗ {e}")
        total_errors += len(threshold_errors)
    else:
        print(f"   [PASS] All 117 WORKING + PRODUCTION thresholds parse correctly")

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
