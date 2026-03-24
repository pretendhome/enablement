# Kiro Scaffold Task: Generate 117 Module Files

## Task Summary
Generate one `module.yaml` file for each of the 117 RIUs in the Palette taxonomy, following the pattern established by the 5 example modules.

## Input Files
- **Taxonomy**: `../../palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml` (117 RIUs)
- **RIU Classification**: `../../palette/buy-vs-build/service-routing/v1.0/riu_classification_v1.0.yaml`
- **Knowledge Library**: `../../palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`
- **Service Routing**: `../../palette/buy-vs-build/service-routing/v1.0/service_routing_v1.0.yaml`
- **Module Schema**: `../curriculum/module-schema.yaml`
- **Generator Prompt**: `module_generator_prompt.md`

## Example Modules (follow these patterns exactly)
1. `curriculum/workstreams/clarify-and-bound/RIU-001/module.yaml` — internal_only, foundation, portfolio
2. `curriculum/workstreams/quality-and-safety/RIU-021/module.yaml` — both, retrieval, portfolio
3. `curriculum/workstreams/core-logic/RIU-510/module.yaml` — internal_only, orchestration, architecture_defense
4. `curriculum/workstreams/quality-and-safety/RIU-082/module.yaml` — both, foundation, service_integration
5. `curriculum/workstreams/adoption-and-change/RIU-603/module.yaml` — internal_only, specialization, portfolio

## Output Structure
```
curriculum/workstreams/
  clarify-and-bound/
    RIU-001/module.yaml    (already exists)
    RIU-002/module.yaml
    RIU-003/module.yaml
    ...
  interfaces-and-inputs/
    RIU-010/module.yaml
    ...
  core-logic/
    RIU-020/module.yaml
    ...
  quality-and-safety/
    RIU-021/module.yaml    (already exists)
    RIU-082/module.yaml    (already exists)
    ...
  ops-and-delivery/
    RIU-060/module.yaml
    ...
  adoption-and-change/
    RIU-603/module.yaml    (already exists)
    ...
```

## Workstream → Directory Mapping
| Workstream | Directory |
|---|---|
| Clarify & Bound | clarify-and-bound |
| Interfaces & Inputs | interfaces-and-inputs |
| Core Logic | core-logic |
| Quality & Safety | quality-and-safety |
| Ops & Delivery | ops-and-delivery |
| Adoption & Change | adoption-and-change |

## Per-Module Generation Steps

For each RIU:

1. **Read the RIU entry** from taxonomy
2. **Read the classification** (internal_only or both)
3. **Find related KL entries** — search knowledge library for entries that reference this RIU ID
4. **If classification is "both"**: read service routing for candidate services
5. **Assign journey_stage** based on workstream and content (see generator prompt)
6. **Generate module.yaml** following the schema and mapping rules
7. **Validate** against module-schema.yaml

## Quality Requirements

Each generated module MUST:
- [ ] Have 3-5 learning objectives starting with action verbs
- [ ] Have 3-5 rubric dimensions with 4 levels each
- [ ] Have 2-3 exercises covering silent/loud/clustered failure modes
- [ ] Have service_context iff classification is "both"
- [ ] Have prerequisites matching the RIU's dependencies field
- [ ] Pass `scripts/integrity.py`
- [ ] Pass `scripts/prerequisite_validator.py`

## Batch Processing

Process in workstream order:
1. Clarify & Bound (RIU-001 through RIU-009) — 5 already exist partially
2. Interfaces & Inputs (RIU-010 through RIU-019)
3. Core Logic (RIU-020 through RIU-039 + RIU-510 series)
4. Quality & Safety (RIU-080 through RIU-088 + RIU-530 series)
5. Ops & Delivery (RIU-060 through RIU-070 + RIU-520 series)
6. Adoption & Change (RIU-200 series + RIU-600 series)

After each batch, run:
```bash
python3 scripts/integrity.py
python3 scripts/prerequisite_validator.py
python3 scripts/coverage_report.py
```

## Do NOT
- Skip exercises — every module needs 2-3
- Use generic learning objectives — derive from the specific RIU problem_pattern
- Copy rubric dimensions between modules — each module's dimensions come from its own success_conditions
- Assign journey_stage arbitrarily — follow the mapping rules in the generator prompt
- Create modules for RIU IDs that don't exist in the taxonomy
