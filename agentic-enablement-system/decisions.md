# Enablement System — Decisions Log

**Project**: Agentic Enablement System
**Location**: `~/fde/enablement/agentic-enablement-system/`

---

## 🚨 OWD-001: Iteration-Based Architecture

**Date**: 2026-03-16
**Decision**: Build the prompt through 8 discrete iterations, each addressing one problem, rather than writing a monolithic prompt in one pass.
**Rationale**: The problem is abstract and hard. Solving one aspect at a time allows course-correction between iterations. Each iteration produces a testable artifact. Different agents (Kiro, Claude Code, Codex) can pick up different iterations based on their strengths.
**Status**: Approved by human

## 🚨 OWD-002: No Names in the System

**Date**: 2026-03-16
**Decision**: The enablement system never hardcodes learner names, company names, or domain-specific details into the reusable framework. Test cases use anonymized references.
**Rationale**: The system must generalize to any person in any enterprise. Hardcoding names creates a system that looks like it was built for one client.
**Status**: Approved by human

## 🚨 OWD-003: Self-Contained Skill Structure

**Date**: 2026-03-16
**Decision**: The enablement system lives as a self-contained directory under `~/fde/enablement/agentic-enablement-system/` — designed to be a reusable tool and skill, not a one-off project.
**Rationale**: Human explicitly requested "a self-contained enablement structure that will be a tool and a skill going forward."
**Status**: Approved by human

## 🔄 TWD-001: LearnerLens Adapted from Education Lenses

**Date**: 2026-03-16
**Decision**: The LearnerLens schema is adapted from LENS-CHILD-001 and LENS-GUIDE-001 (education-alpha) rather than designed from scratch.
**Rationale**: The education lenses are production-quality with input/output contracts, refresh policies, quality checks, and confidence tracking. Reusing the pattern ensures rigor. The adaptation simplifies for adult professionals (no 6-domain assessment, no CASEL scores) while preserving the structural integrity.

## 🔄 TWD-002: Intake Limited to 3-5 Questions

**Date**: 2026-03-16
**Decision**: The intake protocol asks a maximum of 5 questions (preferring 3) rather than a comprehensive survey.
**Rationale**: Real learner conversations show that non-technical users are busy, context-switched, and can spare 20-40 minutes. A long intake form would lose them. The system can fill in gaps over subsequent sessions. Better to have a thin-but-confirmed lens than a comprehensive-but-unvalidated one.

## 🔄 TWD-003: Assessment Scores Are Internal Only

**Date**: 2026-03-16
**Decision**: The system's assessment of the learner (comfort level, risk posture, learning style) is never shown to the learner as a score or rating.
**Rationale**: Showing someone "comfort_level: 1" is patronizing and counterproductive. The assessment exists to help the system calibrate its recommendations, not to label the learner. The education lenses follow the same principle (LENS-CHILD-001 outputs are for the Guide, not the child).

## 🔄 TWD-004: Progress File as Portable State Carrier

**Date**: 2026-03-16
**Decision**: The system's cross-session memory lives in a single learner-owned, plain-language document (the "progress file") rather than in tool-native persistence, a database, or structured YAML.
**Rationale**: Non-CLI learners use web UIs that don't persist conversations. The progress file must be (1) human-readable so the learner can understand and edit it, (2) portable so it works in any AI tool, (3) single-document so there's only one thing to paste. Tool-native memory (Claude Projects, ChatGPT memory) is used as a bonus layer but never as the source of truth. Structured formats (YAML, JSON) violate the language rules — a learner who sees `comfort_level: 2` has been shown a score, which is an Iteration 1 violation.

## 🔄 TWD-005: Assessment Reconstructed, Not Stored

**Date**: 2026-03-16
**Decision**: The system's internal assessment scores (comfort level, risk posture, learning style) are reconstructed from the progress file's narrative at the start of each conversation, not stored in the progress file.
**Rationale**: Storing scores in a learner-visible document violates TWD-003. Storing them in a separate system-only file creates a second artifact the learner must manage. Reconstruction from narrative is possible because the progress file contains session history, wins, blockers, and what the learner has built — sufficient signal to re-derive assessment scores. Fidelity may degrade with terse progress files; the system should err toward fresh evaluation over stale scores.

## 🔄 TWD-006: Engine / Domain Pack Separation

**Date**: 2026-03-16
**Decision**: The enablement system is split into a reusable engine (Layer 1) and swappable domain packs (Layer 2). The engine contains the lens, coaching loop, progress file, verification patterns, safety principles, and language rules. Domain packs contain stage instantiations, translation tables, worked examples, and tool landscapes.
**Rationale**: Every component built in iterations 1-6 was analyzed and none reference "AI," "agentic," or any domain concept at the structural level. The 7 stages from Iteration 3 are a domain-specific instantiation of a universal pattern (Orient → First Use → Retain → Verify → Organize → Extend → Own). Separating engine from content follows the Codex CONTENT_LAYERING.md pattern and enables deployment to any domain without modifying the engine. Validated with three example domain packs (Agentic Enablement, Product Analytics, CRM Automation).

## 🔄 TWD-007: Tier Classification of All Prompt Components

**Date**: 2026-03-16
**Decision**: Every component in PROMPT.md is classified into Palette's three-tier governance model. 13 Tier 1 rules (always true), 12 Tier 2 assumptions (being tested), 12 Tier 3 experiments (speculative). Each Tier 2 assumption has an explicit promotion path with measurable criteria.
**Rationale**: Without tier classification, a future agent cannot distinguish immutable system physics from provisional design choices. This classification enables safe experimentation (change Tier 2/3 freely) while protecting core integrity (Tier 1 requires human approval). Applied Palette's existing promotion criteria from `assumptions.md` Section 9, plus new demotion criteria for when real learner evidence contradicts an assumption.
