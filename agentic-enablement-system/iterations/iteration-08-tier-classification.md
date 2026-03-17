# Iteration 8: Tier Classification

**Date**: 2026-03-16
**Focus**: Which parts of this system are Tier 1 (always true), Tier 2 (assumptions being tested), and Tier 3 (experimental)?
**Problem it solves**: The prompt has grown across 7 iterations. Some parts are grounded in real learner evidence and proven design patterns. Others are reasoned-but-untested. Others are speculative. Without tier classification, a future agent (or a future version of this system) can't tell which parts to trust absolutely, which to test, and which to replace freely.
**Lineage**: Palette three-tier governance (`palette-core.md`, `assumptions.md`, `decisions.md`), Palette promotion criteria (Section 9 of assumptions.md).

---

## Palette's Tier Model (Applied Here)

From `palette-core.md` and `assumptions.md`:

- **Tier 1**: What must always be true. Violating it breaks the system. Requires explicit human approval to change.
- **Tier 2**: What we are currently testing. Provisional. Expected to change. May be rewritten or removed.
- **Tier 3**: Experimental. Not validated beyond initial reasoning. May be deleted without ceremony.

**Promotion criteria** (from assumptions.md Section 9 — all must be met):
1. Consistently improves convergence
2. Reduces ambiguity or failure
3. Remains debuggable
4. Generalizes across domains
5. Introduces no hidden state
6. Human explicitly approves promotion

**Demotion criteria** (added here — these weren't in Palette's model but are needed):
1. A real learner interaction contradicts the assumption
2. A domain pack can't follow the rule without violating a higher-tier rule
3. The rule creates friction that outweighs its benefit (measured by learner dropout, confusion, or time wasted)

---

## Full Classification

### Tier 1: Always True

These are the system's physics. If any of these are violated, the system is no longer functioning as an enablement engine. They have been validated by real learner evidence, by lineage from proven patterns (education lenses, Codex coaching loop), or by the architectural analysis in Iteration 7 confirming they generalize across domains.

| # | Component | Source | Evidence |
|---|---|---|---|
| T1-01 | **Plain language first, always** | Iter 2, Language Rule 1 | Real learner: "I honestly didn't understand much of this" |
| T1-02 | **Show the problem before the solution** | Iter 2, Language Rule 3 | Pedagogical principle; confirmed by learner confusion when concepts were introduced before need |
| T1-03 | **Use their words** | Iter 2, Language Rule 5 | Learner called a steering file "my AI's job description" — system adoption of their language built trust |
| T1-04 | **Never say "it's simple"** | Iter 2, Language Rule 6 | Respect principle; violating it breaks trust with any learner at any level |
| T1-05 | **Assessment scores are internal only** | Iter 1, TWD-003 | Showing "comfort_level: 1" is patronizing. From LENS-CHILD-001 design principle |
| T1-06 | **The coaching loop structure** (Resume → Do → Check → Capture → Advance) | Iter 4 | Adapted from Codex coaching loop (production-tested in interview prep). The 5 steps are universal |
| T1-07 | **Advance requires demonstration, not just understanding** | Iter 4 | "Yeah I get it" is not a pass. From Codex: "advance only after a pass" |
| T1-08 | **The progress file is learner-owned and portable** | Iter 6, TWD-004 | Core architectural constraint. If violated, learner is locked to one tool and loses their data on vendor change |
| T1-09 | **Never oversell certainty about third-party tools/policies** | Iter 5, Safety Principle 1 | Real learner concern: ban anxiety drove major platform decisions |
| T1-10 | **Flag one-way doors** | Iter 5, Safety Principle 4 | From Palette core. Irreversible decisions require explicit confirmation |
| T1-11 | **Glass-box: the learner can always see why** | Palette core | A recommendation without a traceable reason is a black box |
| T1-12 | **The engine/domain pack separation** | Iter 7, TWD-006 | Validated by classifying every component and creating 3 domain packs. The engine has zero domain-specific references |
| T1-13 | **Convergence before execution** | Palette core | Understand the learner before prescribing a path. From Palette's core principle |

**Count**: 13 Tier 1 rules.

---

### Tier 2: Assumptions Being Tested

These are things we believe are right based on evidence and reasoning, but haven't been validated across enough learners, domains, or sessions to be certain. They should be tested, measured, and either promoted to Tier 1 or demoted to Tier 3 (or removed).

| # | Component | Source | Why Tier 2 (not Tier 1) |
|---|---|---|---|
| T2-01 | **The 5 intake questions** | Iter 1 | Tested with one learner. The questions work but the "prefer 3" heuristic and the ordering may need adjustment for different comfort levels |
| T2-02 | **The 7-stage universal progression** (Orient → First Use → Retain → Verify → Organize → Extend → Own) | Iter 7 | Derived by abstracting from one domain pack (Agentic Enablement) and validated with 2 example packs (Analytics, CRM). Not yet tested with real learners in non-agentic domains |
| T2-03 | **Metaphors over definitions** (Language Rule 2) | Iter 2 | Good pedagogical principle but metaphors are culturally dependent (Gap-005 from Iter 2). English-speaking Western business context is assumed |
| T2-04 | **One concept per session** (Language Rule 4) | Iter 2 | Works for 20-40 minute sessions. Unclear if it holds for longer sessions or for learners who prefer faster pacing |
| T2-05 | **The 5 verification patterns** | Iter 6 | Reasoned from first principles, not empirically tested. The selection matrix (which pattern for which activity type) is especially speculative |
| T2-06 | **The progress file format** (5 sections) | Iter 6, TWD-004 | The concept of a progress file is Tier 1 (T1-08). The specific 5-section format is an assumption — it may need more sections, fewer sections, or different organization |
| T2-07 | **Assessment reconstruction from narrative** | Iter 6, TWD-005 | Design bet. We don't know how well the system can reconstruct comfort_level and risk_posture from terse session summaries. May need lightweight encoded hints |
| T2-08 | **The 4 interaction patterns** (stuck, skip, off-script, overwhelmed) | Iter 4 | Cover the most common situations but may be missing others — e.g., "learner disagrees," "learner brings a collaborator," "learner had a bad experience with the tool between sessions" |
| T2-09 | **Backup before building** (Safety Principle 2) | Iter 5 | The principle is sound, but "before building" may be too early for some learners (creates friction before they've built enough to care about losing) |
| T2-10 | **The agentic enablement stage names and activities** (Domain Pack A) | Iter 3 | Tested with one learner. Activities are concrete but the success criteria may be too strict (or too loose) for different comfort levels |
| T2-11 | **Session state schema** (YAML structure from Iter 4) | Iter 4 | The system's internal tracking format. Works in the design but hasn't been used across enough sessions to know if the fields are the right ones |
| T2-12 | **The translation table entries** | Iter 2, 6 | Some are grounded in real quotes ("idk what an agentic context engine is"). Others are hypothesized ("progress file" → "saving your game"). Need learner testing |

**Count**: 12 Tier 2 assumptions.

**Promotion path for each**:

- **T2-01 → T1**: Test intake protocol with 5+ learners across at least 2 domains. If the questions consistently produce usable lenses in <15 minutes, promote.
- **T2-02 → T1**: Deploy to at least 2 non-agentic domains with real learners. If the progression holds without forcing, promote.
- **T2-03 → T1**: Test with non-English or non-Western learners. If metaphors translate or can be swapped without losing the principle, promote.
- **T2-04 → T1**: Test with learners at comfort_level 3+ who have longer sessions. If they still benefit from one-concept pacing, promote. If they prefer acceleration, add a pacing-by-level rule instead.
- **T2-05 → T1**: Track which verification pattern the system uses per session for 20+ sessions. If the selection matrix aligns with actual choices, promote. If the system consistently overrides the matrix, fix the matrix.
- **T2-06 → T1**: After 10+ learners have used progress files across multiple sessions, check: did any section go unused? Did learners add their own sections? Adjust format, then promote.
- **T2-07 → T1**: Compare reconstructed assessments to original assessments for 10+ session pairs. If fidelity is >80%, promote. If not, add lightweight hints to the progress file format.
- **T2-08 → T1**: Log every time a learner interaction doesn't match any of the 4 patterns. After 20+ sessions, if no new pattern is needed, promote. If new patterns emerge, add them first.
- **T2-09 → T1**: Track when learners resist the backup step. If resistance is rare (<10% of learners), promote. If frequent, adjust the timing.
- **T2-10 → T1**: After 5+ learners complete the full agentic enablement path, check success criteria against actual outcomes. Adjust criteria, then promote.
- **T2-11 → T1**: After 20+ sessions, audit which session state fields are actually used vs. ignored. Remove unused fields, add missing ones, then promote.
- **T2-12 → T1**: A/B test: show learners the technical term first vs. the translation first. If translation-first consistently reduces confusion, promote the entries that work.

---

### Tier 3: Experimental

These are ideas introduced in the iterations that haven't been validated at all. They may be wrong. They exist as design proposals, not commitments.

| # | Component | Source | Why Tier 3 |
|---|---|---|---|
| T3-01 | **Domain Pack B: Product Analytics** | Iter 7 | Example only. Never tested with a real PM. Stage activities and translation table are hypothesized |
| T3-02 | **Domain Pack C: CRM Automation** | Iter 7 | Example only. Never tested with a real sales rep |
| T3-03 | **Domain pack creation guide** (5-step process) | Iter 7 | Never been used by anyone to create a domain pack from scratch. May be too rigid or too loose |
| T3-04 | **The "menu of possibilities" concept** | Iter 3, Gap-004 | Referenced repeatedly but never defined. The idea that Stage 1 should show outcomes from other learners is sound but has no content behind it |
| T3-05 | **Progress file pruning strategy** | Iter 6, Gap-001 | Not defined. Session log growth is a known problem with no proposed solution |
| T3-06 | **Multi-learner dashboard** | Iter 6, Gap-002 | Conceptual. Enterprise managers may want aggregate views but the architecture for this doesn't exist |
| T3-07 | **Automated handoff via tool-native features** | Iter 6, Gap-003 | Conceptual. Some tools could automate progress file loading, but no integration patterns have been designed |
| T3-08 | **Cross-domain enablement** (composing multiple domain packs) | Iter 7, Gap-002 | Conceptual. What happens when a learner needs two domain packs simultaneously is undefined |
| T3-09 | **Graduation criteria** | Iter 4, Gap-001 | The coaching loop has no formal "you're done" signal. Stage 7 (Own/Autonomy) is the closest but its success criteria are fuzzy |
| T3-10 | **Restart document template** | Iter 5, Gap-002 | The progress file from Iteration 6 partially fills this, but the "restart document" concept from Safety was about rebuilding the entire system, not just resuming a session |
| T3-11 | **Sensitive data classification guide** | Iter 5, Gap-003 | "Don't put sensitive data in AI tools" is the rule. What counts as "sensitive" for a specific enterprise is undefined |
| T3-12 | **Offline progress detection** | Iter 6, Gap-005 | Conceptual. What the system does when the learner has made progress between sessions without the system present |

**Count**: 12 Tier 3 items.

**Note**: Tier 3 items should not be deleted — they're the backlog. Each one either graduates to Tier 2 (by getting designed and reasoned about) or gets dropped (when evidence shows the problem doesn't matter in practice).

---

## Tier Summary

| Tier | Count | Description | Change policy |
|---|---|---|---|
| **Tier 1** | 13 | Always true. The system's physics. | Requires human approval to change |
| **Tier 2** | 12 | Assumptions being tested. Provisional. | May be updated, promoted, or demoted based on evidence |
| **Tier 3** | 12 | Experimental. Not validated. | May be designed, promoted to Tier 2, or dropped freely |

**Total classified**: 37 items across the full system.

---

## Where This Should Live (Long-Term Placement)

The enablement system currently lives at `~/fde/enablement/agentic-enablement-system/`. The question is: where does it belong in Palette's architecture?

### Recommendation: `palette/skills/enablement/`

**Rationale**:

The system has two layers (Iteration 7):
- **Engine** — The reusable enablement infrastructure (lens, loop, progress file, verification, safety, language rules). This is a **skill** in Palette's architecture — a validated domain framework.
- **Domain packs** — Scenario content. These are the equivalent of skill-specific reference material.

Palette's existing skill structure (`palette/skills/`) already has retail-ai, talent, education, and travel. Enablement fits the same pattern:

```
palette/skills/enablement/
├── engine.md                    # The assembled prompt (current PROMPT.md)
├── decisions.md                 # Decision log (current decisions.md)
├── domain-packs/
│   ├── agentic-enablement.md    # Domain Pack A (current default)
│   ├── product-analytics.md     # Domain Pack B (Tier 3, example)
│   └── crm-automation.md        # Domain Pack C (Tier 3, example)
└── iterations/                  # Build history (current iterations/)
```

**This is a ONE-WAY DOOR decision** — moving the system reorganizes the codebase and changes references. I am recommending it, not executing it. The human decides.

### What gets promoted to a steering file?

The 13 Tier 1 rules could be extracted into a lightweight steering file (like `palette-core.md` is for Palette). This would mean:

- `enablement-core.md` — The 13 Tier 1 rules. Immutable without human approval.
- `engine.md` — The full assembled prompt (Tier 1 + Tier 2). The working system.

**Recommendation**: Not yet. The system hasn't been deployed to enough learners to justify splitting the prompt into two files. A single `engine.md` with tier annotations inline is sufficient. When the system has been used with 10+ learners and the Tier 1 rules have survived unchanged, split them into a steering file.

---

## Tier Annotations for PROMPT.md

Rather than restructure the prompt now, the tiers can be marked inline. The convention:

```
<!-- T1 --> = Tier 1: Always true
<!-- T2 --> = Tier 2: Assumption being tested
<!-- T3 --> = Tier 3: Experimental
```

These annotations are for system maintainers (the agents that update the prompt), not for learners. They should never appear in learner-facing output.

The full annotation map:

| PROMPT.md Section | Tier | Notes |
|---|---|---|
| Who You Are (role definition) | T1 | Three responsibilities are the engine's identity |
| Domain Awareness note | T1 | Engine/domain pack separation is validated (T1-12) |
| Who You Are Enabling (learner description) | T2 | Domain-pack-specific. The agentic enablement learner description is T2-10 |
| Language Rule 1 (plain language first) | T1 | T1-01 |
| Language Rule 2 (metaphors over definitions) | T2 | T2-03 (culturally dependent) |
| Language Rule 3 (show the problem) | T1 | T1-02 |
| Language Rule 4 (one concept per session) | T2 | T2-04 (pacing assumption) |
| Language Rule 5 (use their words) | T1 | T1-03 |
| Language Rule 6 (never say "it's simple") | T1 | T1-04 |
| Translation table (engine terms) | T2 | T2-12 (translations need learner testing) |
| Translation table (domain terms) | T2 | T2-12, domain-pack-specific |
| Section 1: Learner Lens schema | T1 | 4-section structure is validated from education lenses |
| Section 1: Intake questions | T2 | T2-01 (tested with 1 learner) |
| Section 1: Lens rules | T1 | T1-05 (scores internal), convergence before execution |
| Section 2: 7 stages (as listed) | T2 | T2-10 (domain pack A, agentic-specific names) |
| Section 2: Brief generation rules | T1 | All 6 rules are engine-level. They generalize |
| Section 2: "Brief Is Not" | T1 | Anti-pattern definitions. Always true |
| Section 3: Coaching loop (5 steps) | T1 | T1-06 |
| Section 3: "Advance requires demonstration" | T1 | T1-07 |
| Section 3: Interaction patterns (4) | T2 | T2-08 (may be incomplete) |
| Section 3: Session memory list | T2 | T2-11 (fields may change) |
| Section 4: Safety — vendor uncertainty | T1 | T1-09 |
| Section 4: Safety — backup before building | T2 | T2-09 (timing may need adjustment) |
| Section 4: Safety — control distinction | T1 | Always true |
| Section 4: Safety — one-way doors | T1 | T1-10 |
| Section 4: Self-governance rules | T1 | T1-11 (glass-box) |
| Section 5: Progress file concept | T1 | T1-08 |
| Section 5: Progress file format | T2 | T2-06 (5-section format is provisional) |
| Section 5: Session handoff protocol | T2 | T2-06 (paste-at-start pattern is provisional) |
| Section 5: Verification patterns | T2 | T2-05 |

---

## How This Connects to Previous Iterations

**Iteration 1 (LearnerLens)**: Schema structure is Tier 1 (proven lineage from education lenses). Intake questions are Tier 2 (tested with one learner). Assessment internality is Tier 1.

**Iteration 2 (Language Calibration)**: 4 of 6 rules are Tier 1. Rules 2 (metaphors) and 4 (one concept) are Tier 2 due to cultural assumptions and pacing assumptions. Translation table is Tier 2 (needs testing).

**Iteration 3 (Convergence Brief)**: The brief generation rules are Tier 1 (engine-level, they generalize). The 7 specific stage names and activities are Tier 2 (Domain Pack A, agentic-specific). The universal 7-stage pattern from Iteration 7 is Tier 2 (needs multi-domain validation).

**Iteration 4 (Coaching Loop)**: The 5-step loop is Tier 1. The "advance requires demonstration" rule is Tier 1. The 4 interaction patterns are Tier 2 (may be incomplete). Session state schema is Tier 2.

**Iteration 5 (Safety & Governance)**: Vendor uncertainty and one-way door flagging are Tier 1. Backup timing is Tier 2. Self-governance rules (glass-box, mark assumptions) are Tier 1.

**Iteration 6 (Memory & Verification)**: Progress file as learner-owned portable artifact is Tier 1. The specific 5-section format and the 5 verification patterns are Tier 2. Assessment reconstruction is Tier 2.

**Iteration 7 (Generalization)**: Engine/domain pack separation is Tier 1 (validated by analysis). The 7-stage universal pattern is Tier 2 (needs multi-domain testing). Example domain packs B and C are Tier 3. Domain pack creation guide is Tier 3.

---

## Prompt Section (for assembly into PROMPT.md)

This iteration adds a short section to PROMPT.md — a governance note for system maintainers.

```markdown
## System Governance

This prompt is tiered:

- **Tier 1 rules** (like language rules 1, 3, 5, 6, the coaching loop, the progress file
  concept, safety principles, glass-box) are always true. Do not modify them without
  explicit human approval.

- **Tier 2 assumptions** (like specific intake questions, interaction patterns, verification
  pattern selection, the progress file format) are being tested. Update them based on
  evidence from real learner interactions.

- **Tier 3 experiments** (like example domain packs, graduation criteria, cross-domain
  composition) are speculative. Design them, test them, or drop them freely.

When in doubt about whether something is Tier 1 or Tier 2, check: would violating this
rule break the system for any learner in any domain? If yes, it's Tier 1. If it might
break the system for some learners in some domains, it's Tier 2.
```

---

## Gaps

1. **No measurement framework.** The promotion paths for Tier 2 assumptions reference specific thresholds (5+ learners, 20+ sessions, >80% fidelity) but there's no system for actually tracking these metrics. A lightweight measurement approach is needed — probably as simple as a ledger in the progress file or a maintainer-side log.

2. **Tier 1 rules are not yet battle-tested.** They're classified as Tier 1 based on lineage and reasoning, not on extensive field deployment. Honestly, every Tier 1 rule is a Tier 2 assumption that we're treating as Tier 1 because the evidence is strong enough. True Tier 1 status requires surviving deployment to 10+ learners across 2+ domains.

3. **No demotion process for Tier 1 rules.** The promotion criteria from Palette's assumptions.md are well-defined. The demotion criteria proposed in this iteration (learner contradiction, domain pack conflict, friction outweighing benefit) are new and haven't been reviewed by the human.

4. **The "Where This Lives" recommendation is pending.** Moving to `palette/skills/enablement/` is a one-way door flagged for human decision.

---

## Status

**Iteration 8: COMPLETE**
- Every component in PROMPT.md classified into Tier 1, 2, or 3
- 13 Tier 1 rules identified with evidence
- 12 Tier 2 assumptions identified with promotion paths
- 12 Tier 3 experiments cataloged
- Annotation convention defined for inline marking
- Full annotation map provided for PROMPT.md
- Long-term placement recommendation made (palette/skills/enablement/) — flagged as ONE-WAY DOOR
- Prompt section drafted for assembly
- Gaps flagged (4)

**This is the final planned iteration.** The system is now complete as designed (8 iterations). Future work falls into:
- Testing Tier 2 assumptions with real learners
- Designing Tier 3 experiments
- Promoting proven Tier 2s to Tier 1
- Creating new domain packs
