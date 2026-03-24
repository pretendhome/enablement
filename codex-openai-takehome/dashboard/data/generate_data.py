#!/usr/bin/env python3
"""
Deterministic generator for simulated Codex usage data.
Simulated pilot program data, March 10-20 2026 (weekdays only).
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 42
random.seed(SEED)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PILOT_START = datetime(2026, 3, 10)  # Monday
PILOT_END = datetime(2026, 3, 21)    # Saturday (last working day is Friday 20th)

TEAMS = {
    "Platform":  {"engineers": 8, "weight": 0.30},
    "Checkout":  {"engineers": 6, "weight": 0.22},
    "Inventory": {"engineers": 5, "weight": 0.18},
    "Payments":  {"engineers": 5, "weight": 0.17},
    "Mobile":    {"engineers": 4, "weight": 0.13},
}

TOTAL_ENGINEERS = sum(t["engineers"] for t in TEAMS.values())  # 28

WORKFLOWS = {
    "code_understanding": 0.50,
    "test_generation":    0.25,
    "impact_analysis":    0.15,
    "docs_refactoring":   0.10,
}

RISK_LEVELS = {
    "green":  0.70,
    "yellow": 0.25,
    "red":    0.05,
}

IMPACT_CATEGORIES = ["onboarding", "velocity", "quality", "compliance", "debugging"]

TARGET_MODULES = {
    "Platform": [
        "auth/token_expiration",
        "auth/session_manager",
        "auth/oauth_integration",
        "platform/feature_flags",
        "platform/config_service",
        "platform/api_gateway",
    ],
    "Checkout": [
        "checkout/cart_total",
        "checkout/tax_calculation",
        "checkout/promo_engine",
        "checkout/shipping_calculator",
        "checkout/order_confirmation",
    ],
    "Inventory": [
        "inventory/sync_pipeline",
        "inventory/warehouse_api",
        "inventory/stock_allocator",
        "inventory/demand_forecast",
        "inventory/reorder_trigger",
    ],
    "Payments": [
        "payments/pci_tokenizer",
        "payments/refund_processor",
        "payments/fraud_detector",
        "payments/gateway_router",
        "payments/settlement_batch",
    ],
    "Mobile": [
        "mobile/push_notifications",
        "mobile/deep_link_resolver",
        "mobile/offline_cache",
        "mobile/biometric_auth",
    ],
}

# Prompt templates per workflow
PROMPT_TEMPLATES = {
    "code_understanding": [
        "Explain the data flow through {module}",
        "What are the dependencies of {module}?",
        "How does {module} handle edge cases?",
        "Trace the call chain starting from {module}",
        "Summarize the retry logic in {module}",
        "What error handling exists in {module}?",
        "Explain the caching strategy in {module}",
        "How does {module} interact with the database layer?",
        "Walk through the request lifecycle in {module}",
        "What configuration values does {module} depend on?",
        "Identify all external API calls in {module}",
        "Explain the validation rules in {module}",
        "How is state managed across {module} boundaries?",
        "What happens when {module} receives malformed input?",
        "Map the inheritance hierarchy in {module}",
    ],
    "test_generation": [
        "Generate unit tests for {module} happy path",
        "Write integration tests for {module} error scenarios",
        "Create test fixtures for {module} edge cases",
        "Generate regression tests for {module} after recent changes",
        "Write boundary value tests for {module}",
        "Create mock objects for {module} external dependencies",
        "Generate load test scenarios for {module}",
        "Write contract tests for {module} API surface",
    ],
    "impact_analysis": [
        "What breaks if we modify {module} return types?",
        "Assess blast radius of deprecating {module}",
        "Which downstream services depend on {module}?",
        "Impact of changing {module} timeout from 5s to 2s",
        "Risk assessment for migrating {module} to async",
        "What tests cover {module} and what gaps exist?",
        "Evaluate impact of adding rate limiting to {module}",
    ],
    "docs_refactoring": [
        "Generate API documentation for {module}",
        "Create onboarding guide for {module}",
        "Document the deployment runbook for {module}",
        "Write architecture decision record for {module} design",
        "Generate inline documentation for {module} public methods",
        "Create troubleshooting guide for {module} common failures",
    ],
}

# Review status distribution by risk level
REVIEW_STATUS_BY_RISK = {
    "green":  {"approved": 0.92, "pending": 0.06, "rejected": 0.02},
    "yellow": {"approved": 0.60, "pending": 0.25, "rejected": 0.15},
    "red":    {"approved": 0.20, "pending": 0.35, "rejected": 0.45},
}

# Files read/modified ranges by workflow
FILES_BY_WORKFLOW = {
    "code_understanding": {"read": (3, 25),  "modified": (0, 0)},
    "test_generation":    {"read": (4, 15),  "modified": (1, 5)},
    "impact_analysis":    {"read": (8, 40),  "modified": (0, 0)},
    "docs_refactoring":   {"read": (2, 12),  "modified": (1, 4)},
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def weighted_choice(choices_dict):
    """Pick a key from {key: weight} dict using weighted random."""
    keys = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return random.choices(keys, weights=weights, k=1)[0]


def pick_review_status(risk_level):
    dist = REVIEW_STATUS_BY_RISK[risk_level]
    return weighted_choice(dist)


def generate_timestamp(day, hour_weights):
    """Generate a realistic timestamp within a workday."""
    hour = random.choices(range(8, 20), weights=hour_weights, k=1)[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return day.replace(hour=hour, minute=minute, second=second)


def get_day_number(day):
    """Return 1-indexed working day number within the pilot."""
    working_days = []
    d = PILOT_START
    while d < PILOT_END:
        if d.weekday() < 5:  # Mon-Fri
            working_days.append(d.date())
        d += timedelta(days=1)
    try:
        return working_days.index(day.date()) + 1
    except ValueError:
        return 1


def get_workflow_weights(day_number):
    """
    Early days: heavily code_understanding.
    Later days: more test_generation and docs_refactoring.
    """
    # day_number ranges 1..10
    progress = (day_number - 1) / 9.0  # 0.0 to 1.0

    # code_understanding: starts at 72%, ends at 30%
    cu = 0.72 - 0.42 * progress
    # test_generation: starts at 15%, ends at 35%
    tg = 0.15 + 0.20 * progress
    # impact_analysis: starts at 8%, ends at 22%
    ia = 0.08 + 0.14 * progress
    # docs_refactoring: starts at 5%, ends at 13%
    dr = 0.05 + 0.08 * progress

    # Normalize
    total = cu + tg + ia + dr
    return {
        "code_understanding": cu / total,
        "test_generation":    tg / total,
        "impact_analysis":    ia / total,
        "docs_refactoring":   dr / total,
    }


def get_daily_query_count(day_number):
    """
    Ramp up from ~30 on day 1 to ~70 by day 4, then plateau around 60-75.
    """
    if day_number == 1:
        return random.randint(28, 35)
    elif day_number == 2:
        return random.randint(40, 50)
    elif day_number == 3:
        return random.randint(50, 60)
    elif day_number <= 5:
        return random.randint(58, 72)
    else:
        return random.randint(55, 75)


def get_hour_weights():
    """
    Morning-heavy distribution with lunch dip.
    Hours 8-19 (index 0-11).
    """
    return [
        3,   # 8am  - some early starters
        8,   # 9am  - ramp up
        12,  # 10am - peak morning
        11,  # 11am - still high
        4,   # 12pm - lunch dip
        3,   # 1pm  - still low
        9,   # 2pm  - afternoon ramp
        10,  # 3pm  - afternoon peak
        8,   # 4pm  - winding down
        5,   # 5pm  - some late work
        2,   # 6pm  - stragglers
        1,   # 7pm  - rare
    ]


def impact_category_for_workflow(workflow, day_number):
    """Realistic impact category distribution based on workflow and maturity."""
    if workflow == "code_understanding":
        if day_number <= 3:
            # Early days: mostly onboarding
            return weighted_choice({
                "onboarding": 0.60, "debugging": 0.20,
                "velocity": 0.10, "quality": 0.05, "compliance": 0.05,
            })
        else:
            return weighted_choice({
                "onboarding": 0.25, "debugging": 0.25,
                "velocity": 0.25, "quality": 0.15, "compliance": 0.10,
            })
    elif workflow == "test_generation":
        return weighted_choice({
            "quality": 0.45, "velocity": 0.25,
            "compliance": 0.15, "debugging": 0.10, "onboarding": 0.05,
        })
    elif workflow == "impact_analysis":
        return weighted_choice({
            "velocity": 0.30, "compliance": 0.25,
            "quality": 0.20, "debugging": 0.15, "onboarding": 0.10,
        })
    elif workflow == "docs_refactoring":
        return weighted_choice({
            "onboarding": 0.40, "quality": 0.25,
            "velocity": 0.20, "compliance": 0.10, "debugging": 0.05,
        })
    return random.choice(IMPACT_CATEGORIES)


def session_duration(workflow):
    """Realistic session duration in seconds."""
    ranges = {
        "code_understanding": (30, 180),
        "test_generation":    (60, 240),
        "impact_analysis":    (90, 300),
        "docs_refactoring":   (45, 210),
    }
    lo, hi = ranges[workflow]
    # Use a distribution that clusters toward the middle
    return int(random.triangular(lo, hi, lo + (hi - lo) * 0.4))


def codex_response_time(workflow, files_read):
    """Response time correlates with complexity (files read)."""
    base = {
        "code_understanding": 4,
        "test_generation":    8,
        "impact_analysis":    12,
        "docs_refactoring":   5,
    }
    b = base[workflow]
    # Scale with files read, add noise
    raw = b + files_read * 0.5 + random.gauss(0, 3)
    return round(max(3.0, min(45.0, raw)), 1)


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate():
    random.seed(SEED)

    queries = []
    query_id = 1

    # Build list of working days
    working_days = []
    d = PILOT_START
    while d < PILOT_END:
        if d.weekday() < 5:
            working_days.append(d)
        d += timedelta(days=1)

    hour_weights = get_hour_weights()

    # Track which engineers are "active" per team per day (ramp up)
    # Day 1: ~40% of engineers, Day 2: ~60%, Day 3: ~80%, Day 4+: 100%
    activation_schedule = {1: 0.40, 2: 0.60, 3: 0.80}

    for day in working_days:
        day_number = get_day_number(day)
        daily_count = get_daily_query_count(day_number)
        wf_weights = get_workflow_weights(day_number)

        # Determine active engineers per team for this day
        activation_rate = activation_schedule.get(day_number, 1.0)

        active_engineers = {}
        for team, info in TEAMS.items():
            n_active = max(1, int(info["engineers"] * activation_rate))
            # Always include engineer #1, then randomly pick others
            pool = list(range(1, info["engineers"] + 1))
            random.shuffle(pool)
            if 1 not in pool[:n_active]:
                pool.remove(1)
                pool.insert(0, 1)
            active_engineers[team] = sorted(pool[:n_active])

        for _ in range(daily_count):
            # Pick team (weighted)
            team = weighted_choice({t: TEAMS[t]["weight"] for t in TEAMS})

            # Pick engineer from active pool
            eng_pool = active_engineers[team]
            eng_num = random.choice(eng_pool)
            engineer_label = f"{team} Engineer #{eng_num} (Day {day_number})"

            # Pick workflow (day-adjusted weights)
            workflow = weighted_choice(wf_weights)

            # Pick target module
            module = random.choice(TARGET_MODULES[team])

            # Pick prompt
            template = random.choice(PROMPT_TEMPLATES[workflow])
            prompt_summary = template.format(module=module)

            # Risk level
            risk = weighted_choice(RISK_LEVELS)

            # Impact category
            impact = impact_category_for_workflow(workflow, day_number)

            # Files
            fr_lo, fr_hi = FILES_BY_WORKFLOW[workflow]["read"]
            fm_lo, fm_hi = FILES_BY_WORKFLOW[workflow]["modified"]
            files_read = random.randint(fr_lo, fr_hi)
            files_modified = random.randint(fm_lo, fm_hi)

            # Timing
            ts = generate_timestamp(day, hour_weights)
            sess_dur = session_duration(workflow)
            resp_time = codex_response_time(workflow, files_read)

            # Review status
            review = pick_review_status(risk)

            queries.append({
                "id": f"Q-{query_id:04d}",
                "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "team": team,
                "engineer": engineer_label,
                "workflow": workflow,
                "prompt_summary": prompt_summary,
                "target_module": module,
                "risk_level": risk,
                "impact_category": impact,
                "session_duration_seconds": sess_dur,
                "codex_response_time_seconds": resp_time,
                "approval_mode": "on_request",
                "review_status": review,
                "files_read": files_read,
                "files_modified": files_modified,
            })
            query_id += 1

    # Sort all queries by timestamp for realism
    queries.sort(key=lambda q: q["timestamp"])

    # Ensure Q-0001 is a code_understanding query from Platform (demo storytelling)
    for idx, q in enumerate(queries):
        if q["workflow"] == "code_understanding" and q["team"] == "Platform":
            if idx != 0:
                queries[0], queries[idx] = queries[idx], queries[0]
            break

    # Re-assign sequential IDs after sorting
    for i, q in enumerate(queries, 1):
        q["id"] = f"Q-{i:04d}"

    # Build output
    output = {
        "metadata": {
            "pilot_start": "2026-03-10",
            "pilot_end": "2026-03-20",
            "teams": len(TEAMS),
            "total_engineers": TOTAL_ENGINEERS,
            "total_queries": len(queries),
            "generated_with_seed": SEED,
        },
        "queries": queries,
    }

    return output


def print_stats(data):
    queries = data["queries"]
    n = len(queries)
    print(f"Total queries: {n}")

    # Workflow distribution
    print("\nWorkflow distribution:")
    from collections import Counter
    wf_counts = Counter(q["workflow"] for q in queries)
    for wf, count in sorted(wf_counts.items(), key=lambda x: -x[1]):
        print(f"  {wf}: {count} ({count/n*100:.1f}%)")

    # Risk distribution
    print("\nRisk distribution:")
    risk_counts = Counter(q["risk_level"] for q in queries)
    for r, count in sorted(risk_counts.items(), key=lambda x: -x[1]):
        print(f"  {r}: {count} ({count/n*100:.1f}%)")

    # Team distribution
    print("\nTeam distribution:")
    team_counts = Counter(q["team"] for q in queries)
    for t, count in sorted(team_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count} ({count/n*100:.1f}%)")

    # Daily counts
    print("\nDaily query counts:")
    day_counts = Counter(q["timestamp"][:10] for q in queries)
    for day, count in sorted(day_counts.items()):
        print(f"  {day}: {count}")

    # Impact categories
    print("\nImpact categories:")
    impact_counts = Counter(q["impact_category"] for q in queries)
    for ic, count in sorted(impact_counts.items(), key=lambda x: -x[1]):
        print(f"  {ic}: {count} ({count/n*100:.1f}%)")


if __name__ == "__main__":
    data = generate()

    out_path = Path(__file__).parent / "codex_usage.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Wrote {out_path}")
    print(f"File size: {out_path.stat().st_size / 1024:.1f} KB\n")
    print_stats(data)
