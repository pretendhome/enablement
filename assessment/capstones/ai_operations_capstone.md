# AI Operations Capstone

## Title

Production Launch and Day-2 Operations Plan for an LLM Service

## Summary

Create the operational package required to launch and run an LLM-powered service safely in production, including observability, rollback controls, incident handling, and reliability targets.

## Integrated RIUs

- RIU-060
- RIU-061
- RIU-062
- RIU-063
- RIU-064
- RIU-065
- RIU-068
- RIU-069
- RIU-070
- RIU-085

## Target Duration

24-32 hours

## Portfolio Outcome

A deployment and operations package that another team could use to launch, monitor, and support the service.

## Required Deliverables

- `deployment_envelope.md`
- `observability_baseline.md`
- `performance_envelope.md`
- `budget_envelope.md`
- `feature_flag_and_kill_switch_plan.md`
- `environment_parity_checklist.md`
- `canary_plan.md`
- `slo_sli.md`
- `incident_runbook.md`
- `day2_operations_runbook.md`

## Scenario

An AI feature is ready to move from staging to production. Leadership wants a fast launch, but the platform team requires evidence that the service can be observed, rolled back, operated under load, and kept inside cost and latency constraints.

## Three-Layer Evaluation Fit

### Layer 1

- operational artifacts present
- SLO, canary, and rollback sections exist
- runbooks reference actual alerts, gates, and owners

### Layer 2

AI rubric evaluates:

- deployment readiness,
- observability quality,
- rollback and canary discipline,
- reliability target design,
- incident operability,
- cost and latency control.

### Layer 3

Human review required if:

- rollback criteria are weak,
- SLOs are unrealistic,
- on-call ownership is unclear,
- the candidate proposes one-way-door commitments without sufficient safeguards.

## Rubric Dimensions

- `release_readiness`: deployment envelope, parity, and rollback controls are complete
- `observability_and_detection`: logging, metrics, traces, and alerts would make failures visible
- `performance_and_budget_control`: load, latency, and cost constraints are explicit and enforceable
- `safe_rollout_design`: canary and error-budget gates define objective release decisions
- `incident_and_day2_operability`: responders have clear procedures, ownership, and recovery paths

## Thresholds

- `WORKING`: competent on 4/5 dimensions, with mandatory competence in `safe_rollout_design` and `incident_and_day2_operability`
- `PRODUCTION`: expert on 2/5 dimensions, competent on remaining, plus human confirmation of release and rollback discipline
