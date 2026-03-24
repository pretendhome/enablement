# Kiro Task 001: Scaffold Module Files from Taxonomy

**From**: claude.analysis
**To**: kiro.design
**Thread**: Palette Enablement Phase 1
**Type**: execution_request

---

## Context

We are building a developer enablement & certification system that maps 1:1 to the 117 RIUs in the Palette taxonomy. 5 example modules have been built and validated. Your job is to scaffold the remaining 112.

## Key Files to Read First

| File | What It Is |
|---|---|
| `/home/mical/fde/enablement/content/generators/kiro_scaffold_task.md` | **Your full task spec** — batch processing order, quality requirements, validation steps |
| `/home/mical/fde/enablement/content/generators/module_generator_prompt.md` | Field mapping rules: how each RIU field maps to a module.yaml field |
| `/home/mical/fde/enablement/curriculum/module-schema.yaml` | Schema every module.yaml must conform to |
| `/home/mical/fde/enablement/docs/architecture.md` | System architecture for context |

## Example Modules (follow these patterns exactly)

| Module | Classification | Stage | Assessment Type |
|---|---|---|---|
| `/home/mical/fde/enablement/curriculum/workstreams/clarify-and-bound/RIU-001/module.yaml` | internal_only | foundation | portfolio |
| `/home/mical/fde/enablement/curriculum/workstreams/quality-and-safety/RIU-021/module.yaml` | both | retrieval | portfolio |
| `/home/mical/fde/enablement/curriculum/workstreams/core-logic/RIU-510/module.yaml` | internal_only | orchestration | architecture_defense |
| `/home/mical/fde/enablement/curriculum/workstreams/quality-and-safety/RIU-082/module.yaml` | both | foundation | service_integration |
| `/home/mical/fde/enablement/curriculum/workstreams/adoption-and-change/RIU-603/module.yaml` | internal_only | specialization | portfolio |

## Source Data

| Data | Path |
|---|---|
| Taxonomy (117 RIUs) | `/home/mical/fde/palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml` |
| RIU Classification | `/home/mical/fde/palette/buy-vs-build/service-routing/v1.0/riu_classification_v1.0.yaml` |
| Knowledge Library | `/home/mical/fde/palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml` |
| Service Routing | `/home/mical/fde/palette/buy-vs-build/service-routing/v1.0/service_routing_v1.0.yaml` |

## What to Produce

One `module.yaml` per RIU, placed at:
```
enablement/curriculum/workstreams/{workstream-slug}/RIU-{id}/module.yaml
```

Workstream slug mapping:
| Workstream | Directory |
|---|---|
| Clarify & Bound | clarify-and-bound |
| Interfaces & Inputs | interfaces-and-inputs |
| Core Logic | core-logic |
| Quality & Safety | quality-and-safety |
| Ops & Delivery | ops-and-delivery |
| Adoption & Change | adoption-and-change |

## Processing Order

Work in batches by workstream. After each batch, run validation:
```bash
cd /home/mical/fde/enablement
python3 scripts/integrity.py
python3 scripts/prerequisite_validator.py
python3 scripts/coverage_report.py
```

**Suggested first batch**: Clarify & Bound (RIU-002 through RIU-009) — smallest workstream, builds on RIU-001 which already exists.

## Quality Requirements

Each module MUST have:
- 3-5 learning objectives starting with action verbs
- 3-5 rubric dimensions with [insufficient, basic, competent, expert] levels
- 2-3 exercises covering silent/loud/clustered failure modes
- service_context present if and only if classification is "both"
- Prerequisites matching the RIU's dependencies field

## How to Reply

After each batch, write a status update to `/home/mical/fde/enablement/KIRO_STATUS.md` with: modules completed, validation results, any issues found.
