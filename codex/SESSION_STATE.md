# Session State
**Purpose**: Preserve context across sessions and reduce rework.

## Problem

Most learning systems restart too often.
They forget:
- what already passed
- what failed repeatedly
- what phrasing weakened trust
- what still needs pressure testing

## What To Track

For each active track, keep:

- current mode
- current question
- latest score
- pass / refine / reset
- strongest version so far
- most common failure mode
- next variant to test

## Minimal State Template

```text
Track:
Question:
Mode: Build / Pressure / Simulation / Performance
Latest score:
Status: PASS / REFINE / RESET
What worked:
What weakened trust:
Next required improvement:
Next prompt:
```

## Why This Matters

Without state, users:
- repeat already-solved work
- forget the exact weakness
- reread instead of refining

With state, the system can resume cleanly:
- continue the same question
- escalate to a variant
- move to a simulation only when earned

## For Recorded Work

Track separately:

- best spoken version
- best timed version
- delivery issues
- factual-risk issues
- contingency handling

Because a script that passes on paper may still fail in performance.

## Resume Rule

When resuming, do not ask:
- "what do you want to work on?"

Instead ask:
- "resume the last failed question"
- or "resume the next scheduled pressure test"

The system should make the next useful move obvious.
