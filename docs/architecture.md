# Developer Enablement & Certification System: Architecture

## Executive Summary

This system works backwards from Palette's 117 RIUs to teach developers how to build enterprise AI systems. Each RIU is a real problem a developer will face. The enablement system maps each problem to learning objectives, educational content, and assessment criteria — then evaluates competency through performance-based assessment (not multiple choice) scaled by AI-augmented evaluation.

## Core Design Principle

**The 117 RIUs ARE the curriculum.** Each RIU's fields map directly to curriculum components:

| RIU Field | Curriculum Mapping |
|---|---|
| `problem_pattern` | Learning objective |
| `execution_intent` | Activity design |
| `artifacts` | Portfolio requirements |
| `success_conditions` | Assessment rubric dimensions |
| `failure_modes` | Exercise scenarios (silent, loud, clustered) |
| `dependencies` | Prerequisites |
| `reversibility` | Risk classification (one-way door = higher evidence bar) |
| `agent_types` | Collaboration model |
| `workstreams` | Curriculum grouping |

## Architecture Layers

### 1. Competency Taxonomy (from Palette)
117 competency areas organized into 6 workstreams + 5 specialized series. Each area is classified as `internal_only` (80) or `both` (37, requiring external service integration).

### 2. Knowledge Library (from Palette)
163 sourced entries with evidence tiers and learning progressions. Journey stages: foundation → retrieval → orchestration → specialization, with evaluation as a cross-cutting meta-skill.

### 3. Curriculum Graph
Directed acyclic graph mapping RIU → module → assessment → credential. Prerequisites define the traversal order. Learning paths (journeys) are named sequences through the graph.

### 4. Assessment Engine
Three-layer evaluation:
- **Layer 1 — Automated checks**: artifacts present, code runs, sources cited
- **Layer 2 — AI rubric evaluation**: Claude evaluates each dimension with calibration exemplars
- **Layer 3 — Human calibration**: 10% double-scored, rubric adjusted when agreement < 80%

### 5. Certification System
Three tiers mapping to Palette's maturity model:
- **UNVALIDATED**: Learning. Placement test completed.
- **WORKING**: Demonstrated competence on one track (8-15 RIUs + capstone). 2-year validity.
- **PRODUCTION**: Expert across 2+ tracks. Architecture defense. Peer review contributions. 2-year validity.

### 6. Credentialing (Open Badges 3.0)
Credentials issued as Open Badges 3.0 / W3C Verifiable Credentials:
- Cryptographically verifiable without issuer server
- Per-tier badges with competency metadata and ACE extension
- Issued via Accredible (130M+ credentials, OB 3.0 + W3C VC support)
- LinkedIn-linkable, machine-readable competency alignments

## Certification Tracks

| Track | Stage Focus | RIU Count | Key Modules |
|---|---|---|---|
| AI Foundations | foundation | ~12 | RIU-001 through RIU-009 + core basics |
| RAG Engineer | retrieval | ~10 | RIU-021, RIU-026, RIU-027, RIU-032, RIU-033 |
| Agent Architect | orchestration | ~12 | RIU-510 through RIU-514, RIU-029, RIU-022 |
| AI Governance | governance | ~10 | RIU-530 through RIU-535, RIU-080 through RIU-088 |
| AI Operations | ops | ~10 | RIU-060 through RIU-070, RIU-520 through RIU-524 |

## Assessment Philosophy

No multiple choice. Every assessment requires artifacts:
- **Portfolio review**: Submit work products evaluated against rubrics
- **Architecture defense**: Present and defend design decisions
- **Service integration**: Demonstrate tool selection with cost/quality tradeoffs
- **Diagnosis exercises**: Find and fix failures in provided systems

## Item Bank Architecture

Per module:
- **3-5 anchor items**: Human-calibrated, annotated exemplars (Phase 1 target: 350-585 total)
- **15-30 generated items**: AI-generated from anchor patterns, difficulty-calibrated
- **Retired items**: Removed with rationale (staleness, ambiguity, exposure)

Calibration requirements (from LLM-as-judge research):
- 30-50 expert-annotated examples per rubric dimension for production-quality AI evaluation
- AI-human agreement target: >80% (comparable to human inter-annotator agreement)
- Calibration set reviewed quarterly; items flagged when agreement drops below threshold

## Content Pipeline

### Bootstrap
Generate from existing Palette data: extract RIU fields → retrieve related KL entries via RELATIONSHIP_GRAPH → retrieve service routing for "both" RIUs → generate module using content/generators prompts → validate sources against Tier 1/2/3 bar.

### Maintenance
- Source freshness: flag when cited sources update
- Service freshness: flag when pricing/capabilities change
- Assessment freshness: refresh when >30% items seen by >100 developers

## Integrity Checks

1. RIU coverage: 117/117 modules
2. KL utilization: >80% of 163 entries referenced
3. Prerequisite acyclicity: no cycles
4. Difficulty balance: matches KL distribution
5. Source freshness: no sources >24 months without justification
6. Assessment coverage: 3+ anchor items, 15+ total per module
7. AI-human agreement: >80% per LIB-114
8. Journey completeness: all paths traversable end-to-end

## Agent Assignments

| Agent | Role | Deliverables |
|---|---|---|
| **Kiro** | Heavy lifting | 117 module.yaml, 117 rubric.yaml, graph.yaml, ~350 exercise stubs |
| **Codex** | Creative audit | Assessment methodology, coherence audits, 5 journeys, capstones, domain packs |
| **Perplexity** | Research | Certification best practices, competitor analysis, source enrichment |
| **Claude Code** | Architecture | Repo structure, scripts, AI evaluator prompts, integration, finishing |

## Competitive Positioning

Research confirms this system occupies unoccupied territory (see `docs/research/design_implications.md`):

| Capability | Our System | Closest Competitor |
|---|---|---|
| 100% portfolio-based | Yes | CNCF CKA/CKAD (performance-based but not portfolio) |
| LLM-as-judge for human certification | Yes | Nobody (LLM-as-judge used for model eval, not human cert) |
| Competency graph with adaptive pathways | Yes | Nobody (most use linear tracks) |
| Open Badges 3.0 credentials | Yes | Credly issuers (but not combined with AI evaluation) |

Key risk: LLM-as-judge reliability on complex portfolio artifacts is untested at scale. Mitigated by 10% human calibration and anchor item sets.

---

*Architecture designed 2026-03-24 by Claude Code (claude.analysis) with Palette Architect agent.*
*Research-informed updates 2026-03-24 based on certification landscape analysis.*
