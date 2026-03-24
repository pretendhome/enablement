# RAG Engineer Capstone

## Title

Evidence-Grounded Retrieval System for Policy and Knowledge Support

## Summary

Build the design and evaluation package for a RAG system that answers policy questions across heterogeneous document types with measurable retrieval quality and drift monitoring.

## Integrated RIUs

- RIU-001
- RIU-006
- RIU-021
- RIU-026
- RIU-027
- RIU-032
- RIU-033
- RIU-080
- RIU-086
- RIU-524

## Target Duration

28-36 hours

## Portfolio Outcome

A retrieval architecture and quality-control package that could gate a real pilot release.

## Required Deliverables

- `system_scope.md`
- `golden_set.jsonl`
- `retrieval_design.md`
- `reranking_strategy.md`
- `extraction_schema.json`
- `classification_schema.json`
- `contract_tests.md`
- `regression_plan.md`
- `quality_monitoring_plan.md`
- `evaluation_report.md`

## Scenario

An organization wants a RAG assistant over policies, SOPs, and product documentation. Document quality is uneven, ground truth is sometimes ambiguous, and stakeholders need proof that the system improves answer quality rather than merely sounding fluent.

## Three-Layer Evaluation Fit

### Layer 1

- golden set loads correctly
- schema artifacts validate
- evaluation and monitoring plans contain required sections and thresholds

### Layer 2

AI rubric evaluates:

- retrieval strategy quality,
- metric and golden-set design,
- ranking/extraction/classification coherence,
- regression coverage,
- monitoring quality.

### Layer 3

Human review required if:

- ambiguous ground truth is handled weakly,
- quality thresholds are borderline,
- monitoring design would allow silent degradation.

## Rubric Dimensions

- `evaluation_design`: golden set, metrics, and calibration logic reflect real system quality
- `retrieval_architecture`: similarity and reranking choices are justified against the problem shape
- `structured_output_reliability`: extraction and classification designs are schema-bound and measurable
- `regression_and_drift_control`: regression suite and monitoring plan catch likely failure patterns
- `operational_explanation`: the candidate can explain why the proposed system will fail safely and improve over time

## Thresholds

- `WORKING`: competent on 4/5 dimensions, with mandatory competence in `evaluation_design`
- `PRODUCTION`: expert on 2/5 dimensions, competent on remaining, plus human confirmation of ambiguous-case handling
