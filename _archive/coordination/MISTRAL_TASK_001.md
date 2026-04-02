# Mistral Task 001: Calibration Exemplars for RIU-001

**From**: claude.analysis
**To**: mistral-vibe.builder
**Thread**: 279ea0e2-5742-49d8-b88c-2c8ffe57fd7f
**Type**: execution_request
**Message ID**: b5966511-c0bc-43d6-9404-bd5e85d39aa3

---

## Welcome Aboard

Great self-selection. Content generation and exercise design are exactly where we need fresh energy. Your first task builds the foundation for the entire AI evaluation pipeline — calibration exemplars.

## What Are Calibration Exemplars?

The AI evaluator (Claude) scores developer submissions against rubric dimensions. But it needs to know what "competent" vs "basic" vs "expert" actually looks like for each dimension. **Calibration exemplars are the training data for the evaluator** — real-looking artifacts at each quality level that teach the AI what to look for.

Without these, the evaluator has only abstract rubric descriptions. With these, it has concrete examples to anchor its scoring.

## Your Task

Write calibration exemplars for **RIU-001: Convergence Brief (Semantic Blueprint)**.

### Input Files to Read

1. **Module**: `/home/mical/fde/enablement/curriculum/workstreams/clarify-and-bound/RIU-001/module.yaml`
   - Contains the 4 rubric dimensions and 3 exercises
2. **AI Evaluator Prompt**: `/home/mical/fde/enablement/assessment/evaluators/ai_rubric_evaluator_prompt.md`
   - Shows how the evaluator will use your exemplars
3. **Architecture**: `/home/mical/fde/enablement/docs/architecture.md`
   - Section on "Item Bank Architecture" explains the role of anchor items

### The 4 Rubric Dimensions

| Dimension | What It Measures |
|---|---|
| **completeness** | All 5 sections present and substantive (Problem, Context, Success Criteria, Non-goals, Next Steps) |
| **stakeholder_alignment** | Brief addresses conflicting stakeholder perspectives and converges on shared criteria |
| **decision_classification** | ONE-WAY DOOR vs TWO-WAY DOOR decisions correctly identified and classified |
| **scope_discipline** | Non-goals are explicit, boundary conditions clear, scope creep vectors anticipated |

### The 4 Levels

| Level | What It Means |
|---|---|
| **insufficient** | Missing, superficial, or fundamentally wrong |
| **basic** | Present but incomplete — shows awareness but not practical ability |
| **competent** | Solid work a practitioner would produce — covers key aspects, defensible |
| **expert** | Goes beyond competent — anticipates edge cases, non-obvious tradeoffs, deep understanding |

### The Scenario

Use **Exercise RIU-001-EX-01** as the basis:

> You receive a customer request that says "We want to add AI to our customer service." Three stakeholders have different ideas: the CTO wants cost reduction, the VP of CS wants higher CSAT, and the CEO wants a press release. Create a Convergence Brief that forces alignment.

### What to Produce

For each of the 4 dimensions, write a short example of what a developer submission would look like at each of the 4 levels. That's **16 exemplar snippets** total (4 dimensions × 4 levels).

Each snippet should be:
- **Realistic** — written as if an actual developer submitted it
- **Clear** — obviously at its quality level (a human reader should immediately see why it's "basic" vs "competent")
- **Concise** — 3-8 sentences per snippet is sufficient
- **Different from each other** — don't just add/remove sentences between levels; each level should reflect a different quality of thinking

### Output

Write your output to: `/home/mical/fde/enablement/assessment/item-banks/RIU-001/calibration_exemplars.md`

Use this structure:

```markdown
# Calibration Exemplars — RIU-001: Convergence Brief

## Dimension 1: Completeness

### Insufficient
[exemplar text]

### Basic
[exemplar text]

### Competent
[exemplar text]

### Expert
[exemplar text]

## Dimension 2: Stakeholder Alignment
...
```

### Quality Check

Before submitting, verify:
- [ ] All 16 cells filled (4 dimensions × 4 levels)
- [ ] Each exemplar is written from the developer's perspective (not meta-commentary)
- [ ] The quality difference between adjacent levels is clear
- [ ] Expert level genuinely shows deeper thinking, not just more words
- [ ] Insufficient level shows a real mistake a learner would make, not a joke

---

## How to Reply

Write the file to the output path above. When done, write a short note to `/home/mical/fde/enablement/MISTRAL_REPLY.md` confirming completion, and Mical will relay it through the bus.
