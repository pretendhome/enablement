# Palette Developer Enablement & Certification System

A competency-based developer education and certification platform built on the [Palette knowledge architecture](https://github.com/pretendhome/palette). Works backwards from 117 real enterprise AI problems to teach developers how to solve them — with performance-based assessment scaled through AI-augmented evaluation.

---

## What This Is

This system teaches developers how to build enterprise AI systems by mapping each of 117 real problems (competency areas) to learning objectives, educational content, hands-on exercises, and portfolio-based assessment. It is not a course catalog — it is a competency graph where every node is a real problem, every edge is a prerequisite, and every assessment is a demonstration of ability to solve that problem under realistic conditions.

## How It Works

1. **Placement** — Adaptive assessment determines the developer's current stage
2. **Learning path** — Personalized journey through the competency graph
3. **Module** — Each module teaches one competency area (1 RIU = 1 module)
4. **Assessment** — Portfolio-based: produce artifacts, not answer questions
5. **Certification** — Three tiers: UNVALIDATED → WORKING → PRODUCTION

## Architecture

Built on Palette's existing data layers:

| Palette Layer | Enablement Use |
|---|---|
| 117 competency areas (RIUs) | Curriculum backbone — each RIU = 1 learning module |
| 167 knowledge entries | Content source with evidence tiers and learning progressions |
| 69 integration recipes | Service integration exercises for "both" classified modules |
| 9 specialized agents | Evaluation agents + content maintenance |
| Governance tiers | Certification tier model (UNVALIDATED → WORKING → PRODUCTION) |

## Certification Tracks

| Track | Focus | Stage | RIUs |
|---|---|---|---|
| AI Foundations | Core AI development skills | foundation | ~12 |
| RAG Engineer | Retrieval-augmented generation | retrieval | ~10 |
| Agent Architect | Multi-agent orchestration | orchestration | ~12 |
| AI Governance | Safety, compliance, risk | governance | ~10 |
| AI Operations | MLOps, monitoring, deployment | ops | ~10 |

## Assessment Philosophy

No multiple choice. Every assessment requires the developer to produce artifacts — the same artifacts a practitioner would produce in their actual work:

- **Convergence briefs** — can you scope a problem?
- **Golden sets and eval harnesses** — can you measure quality?
- **Architecture designs** — can you design and defend a system?
- **Guardrail implementations** — can you make a system safe?
- **Adoption programs** — can you drive organizational change?

Evaluated by a three-layer system:
1. **Automated checks** — artifacts present, code runs, sources cited
2. **AI rubric evaluation** — Claude evaluates each dimension with calibration exemplars
3. **Human calibration** — 10% double-scored, agreement target >80%

## Existing Enablement Assets

This repo also contains the enablement methodology that informed the certification system:

### Enablement Creation (`codex/`)
Reusable methodology patterns: coaching loops, session state, content layering, video performance patterns. Built and validated through real skill progression cycles.

### Agentic Enablement System (`agentic-enablement-system/`)
Complete coaching system built in 8 iterations — learner profiling, language calibration, learning paths, coaching loops, safety, memory architecture, governance tiers. The engine/domain-pack architecture that informed the certification track design.

## Status

**Phase 1**: Foundation scaffold in progress. Architecture designed. Module schema defined. Agent assignments distributed.

## Built By

Multi-agent collaboration using the [Palette Peers](https://github.com/pretendhome/palette/tree/main/peers) governed message bus:
- **Claude Code** (claude.analysis) — Architecture, orchestration, finishing
- **Kiro** (kiro.design) — Module scaffolding, rubric generation, prerequisite graphs
- **Codex** (codex.implementation) — Assessment methodology, coherence audits, learning paths
- **Perplexity** (perplexity.research) — Certification best practices, competitor analysis

---

*Competency mapped. Knowledge structured. Assessment governed. Scaled through automation.*
