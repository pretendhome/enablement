# Agent Architect Capstone

## Title

Multi-Agent Operations Copilot with Explicit Handoffs and Failure Recovery

## Summary

Design a multi-agent system that triages requests, retrieves relevant context, validates proposed actions, and produces a final operator-ready output with bounded autonomy and recoverable failure handling.

## Integrated RIUs

- RIU-001
- RIU-003
- RIU-021
- RIU-022
- RIU-029
- RIU-082
- RIU-510
- RIU-511
- RIU-512
- RIU-513
- RIU-514
- RIU-062

## Target Duration

32-40 hours

## Portfolio Outcome

A full orchestration design package that demonstrates the candidate can build a safe, auditable, and resilient multi-agent workflow.

## Required Deliverables

- `multi_agent_design.md`
- `agent_catalog.md`
- `prompt_contracts/`
- `message_schema.json`
- `workflow_state_schema.json`
- `tool_allowlist.yaml`
- `guardrails.md`
- `failure_recovery.md`
- `incident_runbook.md`
- `evaluation_plan.md`
- `architecture_defense_brief.md`

## Scenario

An enterprise team wants an agentic copilot that can research an issue, synthesize context, validate proposed changes, and hand a recommendation to an operator. The system must prevent uncontrolled tool use, survive partial failures, and make handoffs observable.

## Three-Layer Evaluation Fit

### Layer 1

- schemas validate
- state, protocol, and allowlist artifacts are complete
- runbook and evaluation plan contain explicit thresholds and escalation rules

### Layer 2

AI rubric evaluates:

- agent boundary quality,
- handoff and protocol clarity,
- state integrity,
- recovery design,
- safety boundaries,
- defense quality.

### Layer 3

Human review required for all production-tier submissions and for any design with borderline capability-boundary or failure-recovery scores.

## Rubric Dimensions

- `workflow_architecture`: agent roles and coordination pattern are coherent and justified
- `contract_and_state_design`: message and state contracts are explicit, validated, and recoverable
- `failure_containment`: retries, degraded modes, and escalation keep failures from cascading
- `capability_safety`: tool and action boundaries are enforceable and auditable
- `evaluation_and_operability`: monitoring, runbook, and evaluation plan make the system operable
- `defense_quality`: candidate can defend design choices under changed constraints

## Thresholds

- `WORKING`: competent on 5/6 dimensions, with mandatory competence in `contract_and_state_design` and `capability_safety`
- `PRODUCTION`: expert on 3/6 dimensions, competent on remaining, plus mandatory human defense review
