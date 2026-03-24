# Module Generator Prompt

You are generating a curriculum module for the Palette Developer Enablement & Certification System. Each module maps 1:1 to a Palette RIU (Reusable Intelligence Unit).

## Input

You will receive:
1. **RIU entry** from `palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`
2. **RIU classification** from `palette/buy-vs-build/service-routing/v1.0/riu_classification_v1.0.yaml`
3. **Related knowledge library entries** from `palette/knowledge-library/v1.4/`
4. **Service routing** (if classification is `both`) from `palette/buy-vs-build/service-routing/v1.0/`

## Output

A complete `module.yaml` conforming to `curriculum/module-schema.yaml`.

## Field Mapping Rules

| RIU Field | Maps To | How |
|---|---|---|
| `riu_id` | `riu_id` | Direct copy |
| `name` | `name` | Direct copy |
| `workstreams[0]` | `workstream` | First workstream |
| `problem_pattern` | `learning_objectives` | Convert problem into 3-5 things a learner must demonstrate they can do |
| `execution_intent` | `exercises` | Each step becomes a teaching activity |
| `artifacts` | `required_artifacts` | What the learner produces for assessment |
| `success_conditions` | `rubric_dimensions` | Each condition becomes a rubric dimension with 4 levels |
| `failure_modes` | `exercises` | Each failure mode (silent/loud/clustered) becomes an exercise |
| `dependencies` | `prerequisites.required` | Direct copy of RIU IDs |
| `reversibility` | Informs `difficulty` | `one_way` = higher difficulty |
| `agent_types` | Informs content | Determines collaboration model taught in module |

## Journey Stage Assignment

Assign `journey_stage` based on workstream and RIU content:
- **foundation**: Clarify & Bound, basic Core Logic, basic Interfaces & Inputs
- **retrieval**: RAG, evaluation, search, embedding-related
- **orchestration**: Multi-agent, workflow, state management, orchestration
- **specialization**: Industry-specific, adoption, multimodal, advanced
- **evaluation**: Cross-cutting evaluation methodology (rare — applies to LIB-113, LIB-114)
- **all**: Applies at every stage (e.g., convergence briefs)

## Learning Objectives

Write 3-5 objectives. Each must:
- Start with an action verb (design, implement, evaluate, defend, identify)
- Be measurable through the assessment
- Map to a specific rubric dimension
- Derive from `problem_pattern` and `execution_intent`

## Rubric Dimensions

Write 3-5 dimensions. Each must:
- Derive from a `success_conditions` field (execution, outcome, safety_quality)
- Have exactly 4 levels: [insufficient, basic, competent, expert]
- Include a clear description of what each level looks like

## Exercises

Write 2-3 exercises. Each must:
- Map to a failure mode from the RIU (silent, loud, clustered)
- Present a realistic scenario a practitioner would face
- Have a clear expected output that demonstrates competency
- Be evaluatable by both AI rubric and human review

## Service Context

For `classification: both` modules:
- List `candidate_services` from service routing
- Include paths to `integration_recipes`
- The assessment should require evaluating service tradeoffs

For `classification: internal_only` modules:
- Set `service_context: null`

## Certification Thresholds

- **WORKING**: Competent on most dimensions (typically 3/4 or 4/5)
- **PRODUCTION**: Expert on majority, competent on rest

## Quality Checks

Before submitting, verify:
- [ ] `riu_id` matches taxonomy entry exactly
- [ ] All learning objectives are measurable
- [ ] All failure modes from RIU are covered by exercises
- [ ] Rubric dimensions map to success conditions
- [ ] Service context is present iff classification is `both`
- [ ] Prerequisites match taxonomy `dependencies` field
- [ ] YAML is valid and conforms to module-schema.yaml
