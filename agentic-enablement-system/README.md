# Agentic Enablement System

**Purpose**: A self-contained enablement tool and skill that helps any non-CLI professional in an enterprise build their own personal agentic software suite — starting from zero.

**Built on**: Palette (three-tier governance, convergence briefs, lenses, coaching loops)
**Test case**: Enabling a non-technical CEO on Palette itself — but the system generalizes to any domain.
**Final vision**: Every employee in a company has their own agentic software suite around themselves.

---

## What This Is

An agentic system with three responsibilities:

1. **Learner Lens** — Build a structured profile of who this person is, what they do, and what they need
2. **Convergence Brief** — Generate a personalized step-by-step enablement path
3. **Enablement Loop** — Run ongoing verification and refinement that keeps the system honest

## What This Is Not

- Not a product for one company or one domain
- Not a CLI tool (all flows must work via chat, web UI, or simple buttons)
- Not a one-shot system (it improves itself through iterations)

---

## Iteration Log

Each iteration addresses one specific problem. Previous iterations are preserved for comparison.

| Iteration | Focus | Status | File |
|---|---|---|---|
| 1 | LearnerLens schema + intake | ✅ Complete | `iterations/iteration-01-learner-lens.md` |
| 2 | Language calibration for non-CLI users | ✅ Complete | `iterations/iteration-02-language-calibration.md` |
| 3 | Convergence Brief structure | ✅ Complete | `iterations/iteration-03-convergence-brief.md` |
| 4 | Coaching Loop integration | ✅ Complete | `iterations/iteration-04-coaching-loop.md` |
| 5 | Safety & governance | ✅ Complete | `iterations/iteration-05-safety-governance.md` |
| 6 | Memory & verification architecture | ✅ Complete | `iterations/iteration-06-memory-verification.md` |
| 7 | Generalization (any team, any domain) | ✅ Complete | `iterations/iteration-07-generalization.md` |
| 8 | Tier classification (what's Tier 1/2/3) | ✅ Complete | `iterations/iteration-08-tier-classification.md` |

## Assembled Prompt

After all iterations, the final assembled prompt lives in:
- `PROMPT.md` — the complete enablement system prompt

Each iteration builds one section. The prompt is assembled incrementally.

---

## Design Principles

1. **No CLI required** — every flow expressible via chat or web UI
2. **No jargon without translation** — if a term would confuse a non-technical user, explain it in plain language first
3. **Convergence before execution** — understand the learner before prescribing a path
4. **Glass-box** — the learner can always see why the system recommended something
5. **Iterative by design** — the system improves itself; the learner's path adapts as they grow
6. **Names are never hardcoded** — the system works for any person in any role

## Lineage

This system draws from:
- `~/fde/enablement/codex/` — Codex coaching loop (orient → narrow → retrieve → judge → repair → advance)
- `~/fde/implementations/education/adaptive-learning-architecture/` — Lens pattern (LENS-CHILD-001, LENS-GUIDE-001), convergence brief pattern, system architecture
- `~/.kiro/steering/palette-core.md` — Three-tier governance, convergence, glass-box architecture
- `~/.kiro/steering/assumptions.md` — Agent archetypes, maturity model
- Real learner conversations — ground truth for where non-CLI users get stuck

## Handoff Context

This project was initiated by Kiro (iteration plan + Iteration 1). Designed for continuation by Claude Code (depth/refinement) and Codex (reframing/strategy). The iteration structure is the contract — each agent picks up the next iteration and produces a concrete artifact.
