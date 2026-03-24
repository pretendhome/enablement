#!/usr/bin/env python3
"""
Layer 2 — Threshold Engine

Parses certification threshold strings from module.yaml files and evaluates
whether a set of dimension scores meets the threshold.

Part of the Layer 2 scoring harness (see LAYER2_HARNESS_SPEC.md section 5).

Handles all threshold patterns found across 117 modules:

WORKING tier:
  - "competent on 3/4 dimensions"
  - "competent on 4/5 dimensions"
  - "competent on 2/3 dimensions"
  - "competent on 3/3 dimensions"
  - "competent on all 3 dimensions, with mandatory competence in information_preservation"
  - "competent on all 4 dimensions, with mandatory competence in token_security and auth_reliability"
  - "competent on all 4 dimensions, with mandatory competence in adversarial_robustness"

PRODUCTION tier:
  - "expert on 3/4, competent on remaining"
  - "expert on 2/4, competent on remaining"
  - "expert on 3/5, competent on remaining"
  - "expert on 2/3, competent on remaining"

Design: fail closed. Unparseable thresholds produce failure results, never silent passes.
Dependencies: Python stdlib + PyYAML.
"""

import re
import yaml
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Level ordering
# ---------------------------------------------------------------------------

LEVELS = ["insufficient", "basic", "competent", "expert"]
LEVEL_RANK = {level: i for i, level in enumerate(LEVELS)}

# Map noun/variant forms to canonical level names.
# The threshold strings use "competence" (noun) in "mandatory competence in ..."
# but the level name is "competent" (adjective).
_LEVEL_ALIASES = {
    "competence": "competent",
}


def _normalize_level(level: str) -> str:
    """Normalize a level string to its canonical form."""
    lower = level.lower().strip()
    return _LEVEL_ALIASES.get(lower, lower)


def level_at_least(actual: str, required: str) -> bool:
    """Return True if actual level is >= required level."""
    actual_rank = LEVEL_RANK.get(_normalize_level(actual))
    required_rank = LEVEL_RANK.get(_normalize_level(required))
    if actual_rank is None or required_rank is None:
        return False
    return actual_rank >= required_rank


# ---------------------------------------------------------------------------
# Rule data structures
# ---------------------------------------------------------------------------

@dataclass
class ThresholdRule:
    """Normalized representation of a parsed threshold string."""

    # The minimum level that counts as "meeting" the primary requirement.
    # For WORKING tiers this is typically "competent".
    # For PRODUCTION tiers this is the higher bar (e.g. "expert").
    primary_level: str

    # How many dimensions must meet primary_level.
    # If required_count == total_count, this is an "all" rule.
    required_count: int

    # Expected total dimension count from the threshold string.
    # Used for validation against actual dimension count.
    total_count: int

    # For PRODUCTION-style rules: the floor level for remaining dimensions.
    # None for WORKING-style rules that have no "remaining" clause.
    remaining_level: Optional[str] = None

    # Mandatory dimensions that MUST individually meet a specific level.
    # Maps dimension_name -> required_level.
    mandatory: dict = field(default_factory=dict)

    # The original threshold string, kept for error messages.
    raw: str = ""


@dataclass
class ThresholdResult:
    """Result of evaluating dimension scores against a threshold rule."""
    passed: bool
    met_dimensions: list  # dimensions that met the primary level
    failed_dimensions: list  # dimensions that did not meet the primary level
    mandatory_met: Optional[bool] = None  # None if no mandatory dimensions
    mandatory_failures: list = field(default_factory=list)
    detail: str = ""


# ---------------------------------------------------------------------------
# Threshold parser
# ---------------------------------------------------------------------------

# Pattern 1: "competent on 3/4 dimensions"
_PAT_SIMPLE = re.compile(
    r"^(?P<level>\w+)\s+on\s+(?P<req>\d+)/(?P<total>\d+)\s+dimensions?$",
    re.IGNORECASE,
)

# Pattern 2: "competent on all 4 dimensions, with mandatory competence in dim1 and dim2"
# Also handles: "competent on all 4 dimensions" (no mandatory clause)
_PAT_ALL_WITH_MANDATORY = re.compile(
    r"^(?P<level>\w+)\s+on\s+all\s+(?P<total>\d+)\s+dimensions?"
    r"(?:,?\s+with\s+mandatory\s+(?P<mandatory_level>\w+)\s+in\s+(?P<dims>.+))?$",
    re.IGNORECASE,
)

# Pattern 3: "expert on 3/4, competent on remaining"
_PAT_SPLIT = re.compile(
    r"^(?P<primary_level>\w+)\s+on\s+(?P<req>\d+)/(?P<total>\d+)"
    r",?\s+(?P<remaining_level>\w+)\s+on\s+remaining$",
    re.IGNORECASE,
)


def _parse_mandatory_dims(dims_str: str) -> list:
    """Parse 'dim1 and dim2' or 'dim1, dim2, and dim3' into a list."""
    # Normalize: replace " and " with comma, then split
    normalized = dims_str.replace(" and ", ", ")
    return [d.strip() for d in normalized.split(",") if d.strip()]


def parse_threshold(threshold_str: str) -> ThresholdRule:
    """
    Parse a threshold string from module.yaml into a ThresholdRule.

    Raises ValueError if the string cannot be parsed (fail closed).
    """
    if not threshold_str or not isinstance(threshold_str, str):
        raise ValueError(f"Empty or non-string threshold: {threshold_str!r}")

    raw = threshold_str.strip()
    # Remove surrounding quotes if present (YAML sometimes preserves them)
    if (raw.startswith('"') and raw.endswith('"')) or \
       (raw.startswith("'") and raw.endswith("'")):
        raw = raw[1:-1].strip()

    # Try Pattern 3 first (split rule) because it's more specific
    m = _PAT_SPLIT.match(raw)
    if m:
        primary_level = _normalize_level(m.group("primary_level"))
        remaining_level = _normalize_level(m.group("remaining_level"))
        if primary_level not in LEVEL_RANK:
            raise ValueError(
                f"Unknown level '{primary_level}' in threshold: {raw}"
            )
        if remaining_level not in LEVEL_RANK:
            raise ValueError(
                f"Unknown level '{remaining_level}' in threshold: {raw}"
            )
        return ThresholdRule(
            primary_level=primary_level,
            required_count=int(m.group("req")),
            total_count=int(m.group("total")),
            remaining_level=remaining_level,
            raw=raw,
        )

    # Try Pattern 2 ("all N dimensions" with optional mandatory)
    m = _PAT_ALL_WITH_MANDATORY.match(raw)
    if m:
        level = _normalize_level(m.group("level"))
        if level not in LEVEL_RANK:
            raise ValueError(f"Unknown level '{level}' in threshold: {raw}")
        total = int(m.group("total"))
        mandatory = {}
        if m.group("mandatory_level") and m.group("dims"):
            mandatory_level = _normalize_level(m.group("mandatory_level"))
            if mandatory_level not in LEVEL_RANK:
                raise ValueError(
                    f"Unknown mandatory level '{mandatory_level}' in threshold: {raw}"
                )
            for dim in _parse_mandatory_dims(m.group("dims")):
                mandatory[dim] = mandatory_level
        return ThresholdRule(
            primary_level=level,
            required_count=total,
            total_count=total,
            mandatory=mandatory,
            raw=raw,
        )

    # Try Pattern 1 (simple N/M)
    m = _PAT_SIMPLE.match(raw)
    if m:
        level = _normalize_level(m.group("level"))
        if level not in LEVEL_RANK:
            raise ValueError(f"Unknown level '{level}' in threshold: {raw}")
        return ThresholdRule(
            primary_level=level,
            required_count=int(m.group("req")),
            total_count=int(m.group("total")),
            raw=raw,
        )

    raise ValueError(f"Cannot parse threshold string: {raw!r}")


# ---------------------------------------------------------------------------
# Threshold evaluator
# ---------------------------------------------------------------------------

def evaluate_threshold(rule: ThresholdRule, scores: dict) -> ThresholdResult:
    """
    Evaluate dimension scores against a parsed ThresholdRule.

    Args:
        rule: A ThresholdRule from parse_threshold().
        scores: Dict mapping dimension_name -> level string.
                e.g. {"stakeholder_coverage": "competent", "ownership_clarity": "expert"}

    Returns:
        ThresholdResult with pass/fail and diagnostics.
    """
    if not scores:
        return ThresholdResult(
            passed=False,
            met_dimensions=[],
            failed_dimensions=[],
            detail="No scores provided",
        )

    # Validate dimension count against rule expectation
    actual_count = len(scores)
    if actual_count != rule.total_count:
        return ThresholdResult(
            passed=False,
            met_dimensions=[],
            failed_dimensions=list(scores.keys()),
            detail=(
                f"Dimension count mismatch: got {actual_count}, "
                f"threshold expects {rule.total_count}"
            ),
        )

    # Validate all score values are recognized levels
    for dim, level in scores.items():
        if level.lower().strip() not in LEVEL_RANK:
            return ThresholdResult(
                passed=False,
                met_dimensions=[],
                failed_dimensions=list(scores.keys()),
                detail=f"Unknown level '{level}' for dimension '{dim}'",
            )

    # Classify dimensions by primary level
    met = []
    failed = []
    for dim, level in scores.items():
        if level_at_least(level, rule.primary_level):
            met.append(dim)
        else:
            failed.append(dim)

    # Check primary count requirement
    primary_pass = len(met) >= rule.required_count

    # Check remaining-level requirement (PRODUCTION-style rules)
    remaining_pass = True
    if rule.remaining_level is not None:
        # Dimensions that didn't meet primary must meet remaining_level
        for dim in failed:
            if not level_at_least(scores[dim], rule.remaining_level):
                remaining_pass = False
                break

    # Check mandatory dimensions
    mandatory_met_flag = None
    mandatory_failures = []
    if rule.mandatory:
        mandatory_met_flag = True
        for dim, required_level in rule.mandatory.items():
            if dim not in scores:
                mandatory_met_flag = False
                mandatory_failures.append(dim)
            elif not level_at_least(scores[dim], required_level):
                mandatory_met_flag = False
                mandatory_failures.append(dim)

    # Overall pass
    passed = primary_pass and remaining_pass
    if mandatory_met_flag is not None:
        passed = passed and mandatory_met_flag

    # Build detail string
    detail = _build_detail(rule, met, failed, mandatory_failures,
                           primary_pass, remaining_pass, mandatory_met_flag)

    return ThresholdResult(
        passed=passed,
        met_dimensions=met,
        failed_dimensions=failed,
        mandatory_met=mandatory_met_flag,
        mandatory_failures=mandatory_failures,
        detail=detail,
    )


def _build_detail(rule, met, failed, mandatory_failures,
                   primary_pass, remaining_pass, mandatory_met_flag):
    """Build a human-readable detail string."""
    parts = []

    # Primary level summary
    if rule.remaining_level:
        # PRODUCTION style
        parts.append(
            f"{len(met)}/{rule.total_count} dimensions at {rule.primary_level} "
            f"(required: {rule.required_count}/{rule.total_count})"
        )
        if not remaining_pass:
            remaining_failures = [
                d for d in failed
                if not level_at_least(
                    # We need scores here but don't have them — use failed list
                    "insufficient",  # placeholder; detail is descriptive
                    rule.remaining_level,
                )
            ]
            parts.append(
                f"not all remaining at {rule.remaining_level}"
            )
    else:
        # WORKING style
        parts.append(
            f"{len(met)}/{rule.total_count} dimensions at "
            f"{rule.primary_level} or above "
            f"(required: {rule.required_count}/{rule.total_count})"
        )

    # Mandatory summary
    if rule.mandatory and mandatory_failures:
        parts.append(
            f"mandatory failures: {', '.join(mandatory_failures)}"
        )
    elif rule.mandatory and mandatory_met_flag:
        parts.append("all mandatory dimensions met")

    return "; ".join(parts)


# ---------------------------------------------------------------------------
# Convenience: check_certification
# ---------------------------------------------------------------------------

def check_certification(module_yaml_path: str, scores: dict) -> dict:
    """
    Load a module.yaml, parse both WORKING and PRODUCTION thresholds,
    evaluate both against the provided scores, and return a full result.

    Args:
        module_yaml_path: Path to a module.yaml file.
        scores: Dict mapping dimension_name -> level string.

    Returns:
        Dict with module id and evaluation results for both tiers.
    """
    with open(module_yaml_path, "r") as f:
        module = yaml.safe_load(f)

    riu_id = module.get("riu_id", "UNKNOWN")
    thresholds = module.get("certification_tier_thresholds", {})

    result = {"module": riu_id}

    for tier in ("WORKING", "PRODUCTION"):
        tier_key = tier.lower()
        threshold_str = thresholds.get(tier)
        if not threshold_str:
            result[tier_key] = {
                "passed": False,
                "met_dimensions": [],
                "failed_dimensions": list(scores.keys()),
                "mandatory_met": None,
                "mandatory_failures": [],
                "detail": f"No {tier} threshold defined in module",
            }
            continue

        try:
            rule = parse_threshold(str(threshold_str))
        except ValueError as e:
            result[tier_key] = {
                "passed": False,
                "met_dimensions": [],
                "failed_dimensions": list(scores.keys()),
                "mandatory_met": None,
                "mandatory_failures": [],
                "detail": f"Threshold parse error: {e}",
            }
            continue

        tr = evaluate_threshold(rule, scores)
        tier_label = tier
        detail_prefix = f"{tier_label}: "
        result[tier_key] = {
            "passed": tr.passed,
            "met_dimensions": tr.met_dimensions,
            "failed_dimensions": tr.failed_dimensions,
            "mandatory_met": tr.mandatory_met,
            "mandatory_failures": tr.mandatory_failures,
            "detail": detail_prefix + tr.detail,
        }

    return result


# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import json

    passed = 0
    failed_tests = 0
    total = 0

    def assert_eq(label, actual, expected):
        global passed, failed_tests, total
        total += 1
        if actual != expected:
            failed_tests += 1
            print(f"  FAIL: {label}")
            print(f"    expected: {expected}")
            print(f"    actual:   {actual}")
        else:
            passed += 1
            print(f"  ok: {label}")

    def assert_true(label, value):
        assert_eq(label, value, True)

    def assert_false(label, value):
        assert_eq(label, value, False)

    # =======================================================================
    print("\n=== PARSE TESTS ===")
    # =======================================================================

    # --- WORKING patterns ---

    print("\n--- Pattern: competent on 3/4 dimensions ---")
    r = parse_threshold("competent on 3/4 dimensions")
    assert_eq("primary_level", r.primary_level, "competent")
    assert_eq("required_count", r.required_count, 3)
    assert_eq("total_count", r.total_count, 4)
    assert_eq("remaining_level", r.remaining_level, None)
    assert_eq("mandatory", r.mandatory, {})

    print("\n--- Pattern: competent on 4/5 dimensions ---")
    r = parse_threshold("competent on 4/5 dimensions")
    assert_eq("required_count", r.required_count, 4)
    assert_eq("total_count", r.total_count, 5)

    print("\n--- Pattern: competent on 2/3 dimensions ---")
    r = parse_threshold("competent on 2/3 dimensions")
    assert_eq("required_count", r.required_count, 2)
    assert_eq("total_count", r.total_count, 3)

    print("\n--- Pattern: competent on 3/3 dimensions ---")
    r = parse_threshold("competent on 3/3 dimensions")
    assert_eq("required_count", r.required_count, 3)
    assert_eq("total_count", r.total_count, 3)

    print("\n--- Pattern: competent on all 3 dimensions, with mandatory competence in information_preservation ---")
    r = parse_threshold("competent on all 3 dimensions, with mandatory competence in information_preservation")
    assert_eq("primary_level", r.primary_level, "competent")
    assert_eq("required_count", r.required_count, 3)
    assert_eq("total_count", r.total_count, 3)
    assert_eq("mandatory", r.mandatory, {"information_preservation": "competent"})

    print("\n--- Pattern: competent on all 4 dimensions, with mandatory competence in token_security and auth_reliability ---")
    r = parse_threshold("competent on all 4 dimensions, with mandatory competence in token_security and auth_reliability")
    assert_eq("primary_level", r.primary_level, "competent")
    assert_eq("required_count", r.required_count, 4)
    assert_eq("total_count", r.total_count, 4)
    assert_eq("mandatory keys", sorted(r.mandatory.keys()), ["auth_reliability", "token_security"])
    assert_eq("mandatory level", r.mandatory["token_security"], "competent")

    print("\n--- Pattern: competent on all 4 dimensions, with mandatory competence in adversarial_robustness ---")
    r = parse_threshold("competent on all 4 dimensions, with mandatory competence in adversarial_robustness")
    assert_eq("mandatory", r.mandatory, {"adversarial_robustness": "competent"})
    assert_eq("total_count", r.total_count, 4)

    # --- PRODUCTION patterns ---

    print("\n--- Pattern: expert on 3/4, competent on remaining ---")
    r = parse_threshold("expert on 3/4, competent on remaining")
    assert_eq("primary_level", r.primary_level, "expert")
    assert_eq("required_count", r.required_count, 3)
    assert_eq("total_count", r.total_count, 4)
    assert_eq("remaining_level", r.remaining_level, "competent")

    print("\n--- Pattern: expert on 2/4, competent on remaining ---")
    r = parse_threshold("expert on 2/4, competent on remaining")
    assert_eq("required_count", r.required_count, 2)
    assert_eq("total_count", r.total_count, 4)

    print("\n--- Pattern: expert on 3/5, competent on remaining ---")
    r = parse_threshold("expert on 3/5, competent on remaining")
    assert_eq("required_count", r.required_count, 3)
    assert_eq("total_count", r.total_count, 5)

    print("\n--- Pattern: expert on 2/3, competent on remaining ---")
    r = parse_threshold("expert on 2/3, competent on remaining")
    assert_eq("required_count", r.required_count, 2)
    assert_eq("total_count", r.total_count, 3)

    # --- Parse error cases ---

    print("\n--- Parse error: garbage string ---")
    try:
        parse_threshold("this is not a threshold")
        assert_true("should have raised ValueError", False)
    except ValueError:
        assert_true("raised ValueError", True)

    print("\n--- Parse error: empty string ---")
    try:
        parse_threshold("")
        assert_true("should have raised ValueError", False)
    except ValueError:
        assert_true("raised ValueError", True)

    print("\n--- Parse error: unknown level ---")
    try:
        parse_threshold("amazing on 3/4 dimensions")
        assert_true("should have raised ValueError", False)
    except ValueError:
        assert_true("raised ValueError", True)

    # =======================================================================
    print("\n\n=== EVALUATE TESTS ===")
    # =======================================================================

    # --- WORKING: competent on 3/4, should pass ---
    print("\n--- WORKING 3/4: pass case ---")
    rule = parse_threshold("competent on 3/4 dimensions")
    scores = {
        "stakeholder_coverage": "competent",
        "ownership_clarity": "expert",
        "escalation_design": "competent",
        "practical_applicability": "basic",
    }
    result = evaluate_threshold(rule, scores)
    assert_true("passed", result.passed)
    assert_eq("met count", len(result.met_dimensions), 3)
    assert_eq("failed count", len(result.failed_dimensions), 1)
    assert_eq("mandatory_met", result.mandatory_met, None)
    assert_true("practical_applicability failed", "practical_applicability" in result.failed_dimensions)

    # --- WORKING: competent on 3/4, should fail (only 2 meet) ---
    print("\n--- WORKING 3/4: fail case ---")
    scores = {
        "stakeholder_coverage": "competent",
        "ownership_clarity": "basic",
        "escalation_design": "basic",
        "practical_applicability": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_eq("met count", len(result.met_dimensions), 2)

    # --- WORKING: expert counts as competent ---
    print("\n--- WORKING 3/4: expert satisfies competent requirement ---")
    scores = {
        "stakeholder_coverage": "expert",
        "ownership_clarity": "expert",
        "escalation_design": "expert",
        "practical_applicability": "insufficient",
    }
    result = evaluate_threshold(rule, scores)
    assert_true("passed", result.passed)
    assert_eq("met count", len(result.met_dimensions), 3)

    # --- WORKING: all 4 with mandatory, pass ---
    print("\n--- WORKING all-4 mandatory: pass case ---")
    rule = parse_threshold("competent on all 4 dimensions, with mandatory competence in adversarial_robustness")
    scores = {
        "policy_and_evidence_design": "competent",
        "implementation_quality": "expert",
        "adversarial_robustness": "competent",
        "service_evaluation": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_true("passed", result.passed)
    assert_true("mandatory_met", result.mandatory_met)
    assert_eq("mandatory_failures", result.mandatory_failures, [])

    # --- WORKING: all 4 with mandatory, fail on mandatory ---
    print("\n--- WORKING all-4 mandatory: fail on mandatory dimension ---")
    scores = {
        "policy_and_evidence_design": "competent",
        "implementation_quality": "competent",
        "adversarial_robustness": "basic",
        "service_evaluation": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_false("mandatory_met", result.mandatory_met)
    assert_true("adversarial_robustness in failures", "adversarial_robustness" in result.mandatory_failures)

    # --- WORKING: all 4 with mandatory, fail on non-mandatory ---
    print("\n--- WORKING all-4 mandatory: fail on non-mandatory dimension ---")
    scores = {
        "policy_and_evidence_design": "basic",
        "implementation_quality": "competent",
        "adversarial_robustness": "competent",
        "service_evaluation": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_true("mandatory_met", result.mandatory_met)
    assert_eq("met count", len(result.met_dimensions), 3)

    # --- WORKING: multiple mandatory dimensions ---
    print("\n--- WORKING all-4 multiple mandatory: pass case ---")
    rule = parse_threshold("competent on all 4 dimensions, with mandatory competence in token_security and auth_reliability")
    scores = {
        "token_security": "expert",
        "auth_reliability": "competent",
        "distributed_coordination": "competent",
        "test_coverage": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_true("passed", result.passed)
    assert_true("mandatory_met", result.mandatory_met)

    # --- WORKING: multiple mandatory, one fails ---
    print("\n--- WORKING all-4 multiple mandatory: one mandatory fails ---")
    scores = {
        "token_security": "expert",
        "auth_reliability": "basic",
        "distributed_coordination": "competent",
        "test_coverage": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_false("mandatory_met", result.mandatory_met)
    assert_eq("mandatory_failures", result.mandatory_failures, ["auth_reliability"])

    # --- PRODUCTION: expert on 3/4, competent on remaining, pass ---
    print("\n--- PRODUCTION 3/4: pass case ---")
    rule = parse_threshold("expert on 3/4, competent on remaining")
    scores = {
        "stakeholder_coverage": "expert",
        "ownership_clarity": "expert",
        "escalation_design": "expert",
        "practical_applicability": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_true("passed", result.passed)
    assert_eq("met count", len(result.met_dimensions), 3)

    # --- PRODUCTION: expert on 3/4, remaining not at competent ---
    print("\n--- PRODUCTION 3/4: remaining below competent ---")
    scores = {
        "stakeholder_coverage": "expert",
        "ownership_clarity": "expert",
        "escalation_design": "expert",
        "practical_applicability": "basic",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)

    # --- PRODUCTION: not enough expert ---
    print("\n--- PRODUCTION 3/4: not enough expert ---")
    scores = {
        "stakeholder_coverage": "expert",
        "ownership_clarity": "expert",
        "escalation_design": "competent",
        "practical_applicability": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_eq("met count", len(result.met_dimensions), 2)

    # --- PRODUCTION: expert on 2/3, competent on remaining ---
    print("\n--- PRODUCTION 2/3: pass case ---")
    rule = parse_threshold("expert on 2/3, competent on remaining")
    scores = {
        "information_preservation": "expert",
        "task_awareness": "expert",
        "multi_session_quality": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_true("passed", result.passed)

    # --- PRODUCTION: all expert satisfies everything ---
    print("\n--- PRODUCTION 2/3: all expert passes ---")
    scores = {
        "information_preservation": "expert",
        "task_awareness": "expert",
        "multi_session_quality": "expert",
    }
    result = evaluate_threshold(rule, scores)
    assert_true("passed", result.passed)
    assert_eq("met count", len(result.met_dimensions), 3)

    # =======================================================================
    print("\n\n=== EDGE CASE TESTS ===")
    # =======================================================================

    # --- Wrong dimension count ---
    print("\n--- Edge: wrong dimension count ---")
    rule = parse_threshold("competent on 3/4 dimensions")
    scores = {
        "dim_a": "competent",
        "dim_b": "competent",
        "dim_c": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_true("detail mentions mismatch", "mismatch" in result.detail.lower())

    # --- Empty scores ---
    print("\n--- Edge: empty scores ---")
    result = evaluate_threshold(rule, {})
    assert_false("passed", result.passed)

    # --- Unknown level in scores ---
    print("\n--- Edge: unknown level in scores ---")
    scores = {
        "dim_a": "competent",
        "dim_b": "competent",
        "dim_c": "amazing",
        "dim_d": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_true("detail mentions unknown", "unknown" in result.detail.lower())

    # --- Exact boundary: competent on 3/4, exactly 3 pass ---
    print("\n--- Edge: exact boundary pass ---")
    scores = {
        "dim_a": "competent",
        "dim_b": "competent",
        "dim_c": "competent",
        "dim_d": "basic",
    }
    result = evaluate_threshold(rule, scores)
    assert_true("passed at exact boundary", result.passed)
    assert_eq("met count", len(result.met_dimensions), 3)

    # --- All insufficient ---
    print("\n--- Edge: all insufficient ---")
    scores = {
        "dim_a": "insufficient",
        "dim_b": "insufficient",
        "dim_c": "insufficient",
        "dim_d": "insufficient",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_eq("met count", len(result.met_dimensions), 0)

    # --- Mandatory dimension not in scores dict ---
    print("\n--- Edge: mandatory dimension missing from scores ---")
    rule = parse_threshold("competent on all 3 dimensions, with mandatory competence in information_preservation")
    scores = {
        "task_awareness": "competent",
        "multi_session_quality": "competent",
        "some_other_dim": "competent",
    }
    result = evaluate_threshold(rule, scores)
    assert_false("passed", result.passed)
    assert_false("mandatory_met", result.mandatory_met)
    assert_true("info_pres in mandatory_failures", "information_preservation" in result.mandatory_failures)

    # --- Quoted threshold string ---
    print("\n--- Edge: quoted threshold string ---")
    r = parse_threshold('"competent on 3/4 dimensions"')
    assert_eq("primary_level", r.primary_level, "competent")
    assert_eq("required_count", r.required_count, 3)

    # =======================================================================
    print("\n\n=== check_certification INTEGRATION TEST ===")
    # =======================================================================

    # Test against real module.yaml
    import os
    test_module = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "curriculum", "workstreams",
        "clarify-and-bound", "RIU-002", "module.yaml",
    )

    if os.path.exists(test_module):
        print(f"\n--- check_certification against {os.path.basename(test_module)} ---")

        # Should pass WORKING, fail PRODUCTION
        scores = {
            "stakeholder_coverage": "expert",
            "ownership_clarity": "competent",
            "escalation_design": "competent",
            "practical_applicability": "basic",
        }
        cert = check_certification(test_module, scores)
        assert_eq("module", cert["module"], "RIU-002")
        assert_true("working passed", cert["working"]["passed"])
        assert_false("production passed", cert["production"]["passed"])

        print("\n  Full result:")
        print(json.dumps(cert, indent=2))

        # Should pass both
        print("\n--- check_certification: both tiers pass ---")
        scores = {
            "stakeholder_coverage": "expert",
            "ownership_clarity": "expert",
            "escalation_design": "competent",
            "practical_applicability": "expert",
        }
        cert = check_certification(test_module, scores)
        assert_true("working passed", cert["working"]["passed"])
        assert_true("production passed", cert["production"]["passed"])

    else:
        print(f"\n  SKIP: test module not found at {test_module}")

    # Test against mandatory module (RIU-082)
    mandatory_module = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "..", "curriculum", "workstreams",
        "quality-and-safety", "RIU-082", "module.yaml",
    )

    if os.path.exists(mandatory_module):
        print(f"\n--- check_certification against RIU-082 (mandatory dims) ---")

        # Pass: all competent including mandatory
        scores = {
            "policy_and_evidence_design": "competent",
            "implementation_quality": "competent",
            "adversarial_robustness": "expert",
            "service_evaluation": "competent",
        }
        cert = check_certification(mandatory_module, scores)
        assert_true("working passed", cert["working"]["passed"])
        assert_true("mandatory_met", cert["working"]["mandatory_met"])

        # Fail: mandatory dimension below threshold
        scores = {
            "policy_and_evidence_design": "competent",
            "implementation_quality": "competent",
            "adversarial_robustness": "basic",
            "service_evaluation": "competent",
        }
        cert = check_certification(mandatory_module, scores)
        assert_false("working passed (mandatory fail)", cert["working"]["passed"])
        assert_false("mandatory_met", cert["working"]["mandatory_met"])

        print("\n  Full result (mandatory fail):")
        print(json.dumps(cert, indent=2))
    else:
        print(f"\n  SKIP: test module not found at {mandatory_module}")

    # =======================================================================
    print("\n\n=== RESULTS ===")
    print(f"Passed: {passed}/{total}")
    if failed_tests:
        print(f"FAILED: {failed_tests}/{total}")
        sys.exit(1)
    else:
        print("All tests passed.")
        sys.exit(0)
