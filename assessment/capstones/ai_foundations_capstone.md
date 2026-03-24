# AI Foundations Capstone

## Title

Operational Readiness Blueprint for an Internal AI Assistant

## Summary

Design the first production-ready blueprint for an internal AI assistant used by one business unit. The candidate must take an ambiguous request and turn it into a bounded, testable, safety-aware delivery package.

## Integrated RIUs

- RIU-001
- RIU-002
- RIU-003
- RIU-005
- RIU-006
- RIU-007
- RIU-008
- RIU-009
- RIU-022
- RIU-080
- RIU-082

## Target Duration

20-28 hours

## Portfolio Outcome

A complete project initiation and controls package that a delivery lead could use to start implementation safely.

## Required Deliverables

- `convergence_brief.md`
- `stakeholder_map.md`
- `decisions.md`
- `phase_plan.md`
- `success_metrics_charter.md`
- `constraint_profile.md`
- `assumptions.md`
- `risk_register.md`
- `prompt_contract.md`
- `contract_test_plan.md`
- `policy_rules.yaml`
- `implementation_readiness_review.md`

## Scenario

A department wants an AI assistant for internal policy and process questions. Stakeholders disagree on whether the first milestone should optimize speed, compliance confidence, or employee satisfaction. The candidate must produce a bounded launch blueprint that clarifies scope, defines success, specifies interfaces, and prevents unsafe rollout.

## Three-Layer Evaluation Fit

### Layer 1

- artifacts present and named correctly
- prompt contract and policy YAML parse
- required sections exist in the brief, risk register, and test plan

### Layer 2

AI rubric evaluates:

- scoping quality,
- stakeholder alignment,
- decision traceability,
- measurement quality,
- interface clarity,
- safety-control design.

### Layer 3

Human review required if:

- safety controls are borderline,
- the phase plan includes one-way-door commitments,
- stakeholder conflicts remain unresolved.

## Rubric Dimensions

- `problem_framing`: scope, non-goals, and delivery phases are explicit and defensible
- `decision_governance`: ownership, one-way-door handling, and escalation are clear
- `measurement_design`: metrics and acceptance checks reflect actual business value
- `interface_and_test_readiness`: prompt contract and contract tests are specific enough to implement
- `safety_controls`: evidence requirements, refusal conditions, and tool-use constraints are credible

## Thresholds

- `WORKING`: competent on 4/5 dimensions, with no score below basic
- `PRODUCTION`: expert on 2/5 dimensions, competent on remaining, plus human sign-off on safety controls
