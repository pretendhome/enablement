# Developer Enablement System

14 hands-on learning paths that teach enterprise AI skills by building real artifacts. Each path is a self-contained exercise: paste it into any AI tool (Claude, ChatGPT, Cursor) and build something in 5 minutes to an hour. No slides, no multiple choice — just the work a practitioner actually does.

**Design principle**: structure the knowledge right and the learning works. Every path is organized around what the learner needs to build, not what the system needs to categorize. The curriculum, assessment, and sequencing all follow from that.

## Try It Now

Pick a path, copy the text, paste it into your AI tool, and start building:

| Path | What You Build |
|------|---------------|
| [Tiny AI Eval Harness](paths/RIU-021-tiny-ai-eval-harness.md) | A working eval harness that scores LLM output against a golden set |
| [LLM Safety Guardrails](paths/RIU-082-llm-safety-guardrails.md) | Input/output guardrails with toxicity detection and PII filtering |
| [Multi-Agent Workflow Design](paths/RIU-510-multi-agent-workflow-design.md) | An agent orchestration spec with routing, handoff, and failure modes |

See a complete assessment with rubric and evaluation: [RIU-002 Golden Path Example](examples/RIU-002-golden-path/)

## All Published Paths

| RIU | Path | What It Covers |
|-----|------|---------------|
| 001 | [Convergence Brief](paths/RIU-001-convergence-brief.md) | Scoping an AI problem into a one-page decision doc |
| 021 | [Tiny AI Eval Harness](paths/RIU-021-tiny-ai-eval-harness.md) | Building an eval pipeline with golden sets and scoring |
| 022 | [Prompt Interface Contract](paths/RIU-022-prompt-interface-contract.md) | Defining prompt I/O contracts with version control |
| 035 | [Caching Strategy](paths/RIU-035-caching-strategy.md) | LLM caching design with invalidation and cost modeling |
| 060 | [Deployment Readiness](paths/RIU-060-deployment-readiness-envelope.md) | Go/no-go deployment checklists for AI systems |
| 082 | [LLM Safety Guardrails](paths/RIU-082-llm-safety-guardrails.md) | Input/output safety layers and content filtering |
| 102 | [Enablement Pack](paths/RIU-102-enablement-pack.md) | Writing docs, examples, and how-to guides for AI tools |
| 252 | [Model Evaluation & Selection](paths/RIU-252-model-evaluation-selection.md) | Comparing models on cost, latency, and quality |
| 400 | [KB Content Audit](paths/RIU-400-kb-content-audit.md) | Auditing a knowledge base for coverage and quality |
| 401 | [Taxonomy Design](paths/RIU-401-taxonomy-design.md) | Building a classification taxonomy from scratch |
| 510 | [Multi-Agent Workflow](paths/RIU-510-multi-agent-workflow-design.md) | Designing agent orchestration with routing and handoff |
| 524 | [Output Quality Monitoring](paths/RIU-524-llm-output-quality-monitoring.md) | Setting up LLM output quality checks in production |
| 543 | [Drift Detection](paths/RIU-543-drift-detection.md) | Configuring model and data drift alerts |
| 600 | [Multi-Brand AI Strategy](paths/RIU-600-multi-brand-ai-strategy.md) | AI strategy across multiple brands or business units |

## Architecture

Built on the [Palette](https://github.com/pretendhome/palette) knowledge architecture. Each learning path maps to a competency area (RIU) in the taxonomy:

| Palette Layer | Enablement Use |
|---|---|
| 121 competency areas (RIUs) | Curriculum backbone -- each RIU = 1 learning module |
| 176 knowledge entries | Content source with evidence tiers and learning progressions |
| 69 integration recipes | Service integration exercises for hands-on modules |
| Governance tiers | Certification tier model (UNVALIDATED / WORKING / PRODUCTION) |

The full coaching methodology lives in `agentic-enablement-system/` -- learner profiling, language calibration, learning paths, coaching loops, safety, memory architecture, and governance tiers.

## Certification Tracks

| Track | Focus | Stage | Target RIUs |
|---|---|---|---|
| AI Foundations | Core AI development skills | foundation | ~12 |
| RAG Engineer | Retrieval-augmented generation | retrieval | ~10 |
| Agent Architect | Multi-agent orchestration | orchestration | ~12 |
| AI Governance | Safety, compliance, risk | governance | ~10 |
| AI Operations | MLOps, monitoring, deployment | ops | ~10 |

## Assessment Philosophy

No multiple choice. Every assessment requires producing the same artifacts a practitioner builds in their actual work:

- **Convergence briefs** -- can you scope a problem?
- **Eval harnesses and golden sets** -- can you measure quality?
- **Architecture designs** -- can you design and defend a system?
- **Guardrail implementations** -- can you make a system safe?
- **Enablement packs** -- can you drive organizational adoption?

Evaluated by three layers: automated checks (artifacts present, code runs), AI rubric evaluation (calibrated against exemplars), and human calibration (10% double-scored, >80% agreement target).

## Run the Validators

```bash
pip install -r requirements.txt

# Module integrity (schema, traceability, KL wiring)
python3 scripts/integrity.py

# Curriculum coverage report
python3 scripts/coverage_report.py

# Prerequisite graph validation (cycle detection)
python3 scripts/prerequisite_validator.py

# Constellation integrity (path ordering, completeness)
python3 scripts/constellation_integrity.py
```

## Structure

```
paths/                  14 self-contained learning paths (the main content)
examples/               Golden path assessment example (RIU-002)
curriculum/             121 module specs (one per competency area)
assessment/             Rubrics, evaluators, threshold engine
certification/          Tier and track definitions
agentic-enablement-system/  Coaching methodology and content engine
scripts/                Validation and reporting tools
```

## License

[MIT](LICENSE)

---

Part of the [Palette](https://github.com/pretendhome/palette) intelligence system. Multi-agent development used Claude Code, Kiro, Codex, and Perplexity -- coordination artifacts archived in `_archive/`.
