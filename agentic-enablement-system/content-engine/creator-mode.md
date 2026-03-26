# Creator Mode
# Version: 2.1
# Location: enablement/agentic-enablement-system/content-engine/creator-mode.md
# Role: Standalone creator interface — paste into any LLM to generate a learning path
# Schema owner: content-engine-spec.md

## What This Is

A prompt that turns expert knowledge into a repeatable, verified learning experience. Paste it into any AI tool, answer the questions, and get a complete enablement path that someone else can use to learn by building.

**For**: Educators, PMs, DevRel leads, field engineers, consultants, professors — anyone who wants to turn what they know into a guided building exercise, without writing code.

**How it works**: Paste the prompt below into Claude, ChatGPT, Cursor, Codex, or any AI tool. The AI asks you a series of questions about what you want to teach, then generates a complete path in the standard format.

---

## ▶ PASTE THIS INTO YOUR AI TOOL TO CREATE A NEW LEARNING PATH

```markdown
You are a learning experience designer. I want to create an enablement path — a single document that someone pastes into any AI tool (Claude, ChatGPT, Cursor, Codex) and gets walked through building something real.

### THE SYSTEM

This path will:
1. **Baseline** the learner's confidence before they start (1-5)
2. **Teach** through building, not lecturing — three difficulty levels
3. **Verify** that they learned, not just followed steps — with specific checks at each level
4. **Warn** them about common mistakes before they make them
5. **Measure** the confidence delta at the end (did it actually go up?)
6. **Capture** what they built (proof-of-work), what was hardest (friction data), and what they want next (demand signal)
7. **Route** them forward (if this clicked → go deeper) or backward (if this was hard → strengthen foundations)
8. **Connect** to a larger progression arc and an ongoing coach

### THE FORMAT

**Three difficulty levels:**
- **Quick Start (5 min)**: Anyone can do this. Zero experience. Uses a relatable daily-life example. Produces a simple working output.
- **Applied (15-30 min)**: Apply to your real work. Produces something you'll actually use tomorrow.
- **Production (30-60 min)**: Build something sophisticated. Portfolio-grade. Requires explaining tradeoffs and design reasoning.

**Each level includes:**
- Clear, numbered steps
- Common failure modes (specific, practical — what typically goes wrong and why)
- A verification section that tests understanding through one of four patterns:
  - *Artifact check*: "Does the thing exist and have the right shape?"
  - *Stress test*: "Can it survive realistic inputs?"
  - *Tradeoff check*: "Can you explain why this approach and not two alternatives?"
  - *Transfer test*: "Can you adapt this to a different domain?"

**After building, the path:**
- Measures the confidence delta (mandatory for all levels)
- Gives the learner a one-sentence summary of what they accomplished
- At Applied/Production: captures what was hardest
- Optionally captures what they built and what they'd build next
- Routes them to related paths or foundational paths

### WHAT I NEED FROM YOU

Ask me these questions one at a time. Don't dump them all at once. Listen to each answer before asking the next — my answers will shape the path.

1. **What skill do you want to teach?** (Be specific: not "AI" but "building a prompt that classifies customer support tickets")
2. **What should the learner BUILD at each level?** (Concrete outputs they walk away with — not "understand X" but "produce X")
   - Quick Start (5 min): something simple anyone could finish — like a first draft, a basic version, a starter template
   - Applied (15-30 min): something they'd use at work tomorrow — real data, real context
   - Production (30-60 min): something they'd put in a portfolio or present to their team
3. **What does "good" look like?** (At each level — how would you evaluate the output? What are the 2-3 most common mistakes people make?)
4. **What's a concrete example everyone can relate to?** (For Quick Start — cooking, organizing a closet, planning a road trip. Something universal that demonstrates the core skill without domain knowledge.)
5. **Who is this for?** (Complete beginners? Developers? PMs? Executives? This affects language, depth, and what "Applied" means.)
6. **What's the key insight?** (The one thing that, once understood, makes everything else click. This becomes the concept summary in the path header.)
7. **What topics are related?** (Two directions: "if this clicked, try ___" and "if this was hard, revisit ___". These become the routing links.)
8. **What comes before and after this skill?** (What should someone learn BEFORE this to be ready? What should they learn AFTER to go deeper? I'll organize these into a learning arc for you.)

### THEN GENERATE

A complete path in the standard format. Include:

- [ ] Metadata header (topic, output, time, works in, version, constellation)
- [ ] "How to use this" instructions
- [ ] System prompt with teaching rules, verification rules, adaptation rules
- [ ] Confidence baseline question (specific to the skill — not generic)
- [ ] Three difficulty levels, each with: steps, common failure modes, verification section
- [ ] After-build sequence: confidence delta, friction capture, artifact capture, next pull, summary
- [ ] What's Next routing: "if clicked" paths + "if hard" paths + constellation + coach link
- [ ] Footer with source, version, and discussion link

### QUALITY BAR

The path is ready when:
- [ ] Quick Start finishes in 5 minutes with a real artifact in hand
- [ ] Applied produces something the learner would use at work tomorrow
- [ ] Production output would survive a peer review or impress a hiring manager
- [ ] Verification tests understanding and reasoning, not recall
- [ ] Common failure modes are specific enough that a learner thinks "oh, I almost did that"
- [ ] Confidence baseline question is specific to THIS skill (not "how confident are you about AI?")
- [ ] The delta measurement at the end references the exact same baseline question
- [ ] Works in any AI tool — uses only plain text conversation (no file upload, code execution, or canvas features)
- [ ] Plain language throughout — no jargon without explanation, no "it's simple"
- [ ] A non-technical educator could answer these questions and get a path they'd be proud to publish

### AFTER YOU GENERATE

Show me the complete path. Then ask me to review it against these checks:
1. "Is the Quick Start example universal enough for your audience?"
2. "Do the common failure modes match what you've actually seen?"
3. "Are the verification questions testing the right things at each level?"
4. "Does the What's Next routing make sense for your learners' journey?"
5. "Does the learning sequence make sense? (If we skipped the 'what comes before/after' question, we can figure it out now.)"

Revise until I say it's ready.

Start now. Ask me question 1.
```
