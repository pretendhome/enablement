# Codex Task 001: Assessment Methodology, Journeys, Coherence Audit, Capstones

**From**: claude.analysis
**To**: codex.implementation
**Thread**: Palette Enablement Phase 1
**Type**: execution_request

---

## Context

We are building a developer enablement & certification system with 117 competency areas, portfolio-based assessment, and AI-augmented evaluation. Phase 1 scaffold is complete. Your job is the creative design layer — assessment methodology, learning journeys, coherence audit, and capstone projects.

## Key Files to Read First

| File | What It Is |
|---|---|
| `/home/mical/fde/enablement/docs/architecture.md` | System architecture — 6 layers, assessment philosophy, competitive positioning |
| `/home/mical/fde/enablement/docs/research/design_implications.md` | Research-informed design decisions |
| `/home/mical/fde/enablement/docs/research/certification_best_practices.md` | Competitive landscape (15 programs analyzed) |
| `/home/mical/fde/enablement/assessment/evaluators/ai_rubric_evaluator_prompt.md` | How AI evaluation works |
| `/home/mical/fde/enablement/curriculum/module-schema.yaml` | Module schema |

## Example Modules (read all 5)

- `/home/mical/fde/enablement/curriculum/workstreams/clarify-and-bound/RIU-001/module.yaml`
- `/home/mical/fde/enablement/curriculum/workstreams/quality-and-safety/RIU-021/module.yaml`
- `/home/mical/fde/enablement/curriculum/workstreams/core-logic/RIU-510/module.yaml`
- `/home/mical/fde/enablement/curriculum/workstreams/quality-and-safety/RIU-082/module.yaml`
- `/home/mical/fde/enablement/curriculum/workstreams/adoption-and-change/RIU-603/module.yaml`

## Deliverable 1: Assessment Methodology

**Output**: `/home/mical/fde/enablement/assessment/METHODOLOGY.md`

Write the complete assessment methodology covering:

1. **Portfolio-based assessment philosophy** — why no multiple choice, what makes this approach stronger than MCQ (cite CNCF CKA/CKAD and HashiCorp Professional from the research as validation)
2. **Three-layer evaluation pipeline** — automated checks → AI rubric → human calibration. How each layer works, what it catches, when submissions escalate.
3. **Item bank architecture** — anchor items (human-calibrated exemplars), generated items (AI-maintained from anchor patterns), retired items. How the bank grows and stays fresh.
4. **Inter-rater reliability** — target >80% AI-human agreement. Calibration procedure: 30-50 expert-annotated examples per dimension. What happens when agreement drops.
5. **Adaptive difficulty** — how items adjust based on performance data. Future CAT implementation path (requires 300-500 calibrated items per track).
6. **Integrity measures** — how we prevent gaming (architecture defense for PRODUCTION tier, submission uniqueness checks, AI-generated submission detection).

## Deliverable 2: Five Learning Journeys

**Output**: `/home/mical/fde/enablement/curriculum/journeys/` (one file per journey)

Design 5 certification track paths through the competency graph:

| Track | File | Stage Focus | Target RIUs |
|---|---|---|---|
| AI Foundations | `ai_foundations.yaml` | foundation | ~12 |
| RAG Engineer | `rag_engineer.yaml` | retrieval | ~10 |
| Agent Architect | `agent_architect.yaml` | orchestration | ~12 |
| AI Governance | `ai_governance.yaml` | governance | ~10 |
| AI Operations | `ai_operations.yaml` | ops | ~10 |

Each journey should specify:
- Entry requirements (placement stage, prerequisites)
- Module sequence with rationale for ordering
- Capstone project reference
- Estimated total duration
- Key RIU IDs included

Use the taxonomy at `/home/mical/fde/palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml` to select RIUs per track. Reference the architecture doc's certification tracks table for guidance.

## Deliverable 3: Coherence Audit

**Output**: `/home/mical/fde/enablement/docs/coherence_audit.md`

Systematic audit of the 5 example modules checking:

1. Do learning objectives actually map to rubric dimensions? (each objective should be measurable by at least one dimension)
2. Do exercises cover the failure modes from the RIU? (silent/loud/clustered should all appear)
3. Are assessment types appropriate for the module content?
4. Are prerequisites in the right order? (no circular dependencies, appropriate difficulty progression)
5. Are certification thresholds calibrated consistently across modules?

For each finding, provide: what's wrong, why it matters, and a specific fix.

## Deliverable 4: Capstone Projects

**Output**: `/home/mical/fde/enablement/assessment/capstones/` (one file per track)

Design 5 capstone projects, one per certification track. Each capstone should:
- Require integrating skills from multiple modules in that track
- Produce a substantial portfolio piece (the kind of work a certified developer would do)
- Take 20-40 hours
- Be evaluatable by the 3-layer assessment system
- Have clear rubric dimensions and WORKING/PRODUCTION thresholds

## How to Reply

Write deliverables to their specified output paths. When done (or after each deliverable), write a status update to `/home/mical/fde/enablement/CODEX_STATUS.md`.
