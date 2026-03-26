# UX Review: video-enablement.md v2.0
**Date:** 2026-03-25
**Reviewer:** Kiro (kiro.design)
**Task:** KIRO_TASK_002 — Persona-based UX review
**File reviewed:** `enablement/agentic-enablement-system/content-engine/video-enablement.md`

---

## Persona 1: Complete Beginner

*A teacher who just watched a YouTube video about AI. Has pasted a recipe question into ChatGPT once. Wants to try Quick Start.*

### What works well

- The "How to use this" section is genuinely 5 steps. Numbered. Short. This is the right instinct — don't explain, just tell them what to do.
- "Never say 'it's simple'" in the teaching rules is excellent. Beginners notice when you say that and they're struggling.
- The Quick Start taxonomy example (kid's sports activities, recipes, streaming watchlist) is perfect — universal, zero domain knowledge required.
- The confidence baseline is specific and concrete ("organize a messy domain into clean, non-overlapping categories that someone else could use") — not vague like "how confident are you about taxonomies?"
- Common failure modes at Quick Start level are genuinely the mistakes beginners make. "Organizing by how things feel instead of what they are" — that's real.

### What's confusing or would break the flow

**1. "Start a new conversation" assumes they know what that means.**
A beginner who's used ChatGPT once might not distinguish between a "new conversation" and typing in the existing one. In Claude, it's the "+" button. In ChatGPT, it's "New chat." In Cursor, there's no obvious "conversation" — it's a chat panel or composer. This instruction is tool-specific despite the skill claiming tool-agnosticism.

**2. No preparation for what happens after pasting.**
They paste a wall of text. Then what? The LLM will respond with the "BEFORE WE START" questions. But the beginner doesn't know that. They might think they did something wrong when the AI starts asking them questions instead of teaching. A single sentence of expectation-setting is missing.

**3. The copy boundary is ambiguous.**
Step 3 says "Copy everything below the line." Which line? There are multiple horizontal rules in the document. The `▶ START HERE` marker helps, but the instruction says "below the line" (singular) while the marker says "PASTE EVERYTHING BELOW." A beginner scanning quickly might copy from the wrong point — especially if they copy from "How to use this" downward (which includes the instructions themselves, not just the prompt).

**4. "Artifact check" in the verification section.**
The word "artifact" means nothing to a beginner. They built a list of categories. Calling it an "artifact" makes it sound like they were supposed to produce something more formal. The verification section headers (Artifact check, Reasoning check) read like internal QA labels, not learner-facing language.

**5. The metadata header is intimidating.**
```
> **Source**: RIU-401 | Knowledge: LIB-045, LIB-067
> **Version**: 2026-03-25 | Status: current
> **Path constellation**: Organize → Retrieve → Route (1 of 3)
```
A beginner sees "RIU-401" and "LIB-045" and thinks "this isn't for me." These are system internals. They're useful for Palette's routing but they're noise for a learner. The constellation name is fine — it's descriptive. The IDs are not.

**6. Wall of text problem.**
The full paste (from START HERE to the footer) is ~2,500+ words. When a beginner pastes this into ChatGPT, it works fine. But in some tools (especially mobile), this is a LOT of text in one message. There's no warning about this, and no reassurance that "yes, it's supposed to be this long."

### Specific suggested fixes

**Fix 1** — Replace "Start a new conversation" with tool-aware language:
```
Before:
2. Start a new conversation

After:
2. Start a fresh chat (in ChatGPT: "New chat" | in Claude: click "+" | in Cursor: open a new chat panel)
```

**Fix 2** — Add expectation-setting after step 5:
```
Before:
5. Follow the guide — it walks you through everything

After:
5. Follow the guide — it will ask you a couple of questions first, then walk you through building step by step
```

**Fix 3** — Make the copy boundary unambiguous:
```
Before:
3. Copy everything below the line

After:
3. Copy everything from "▶ START HERE" to the end of this page
```

**Fix 4** — Replace "Artifact check" with plain language in Quick Start verification:
```
Before:
1. **Artifact check**: Does it exist and have the right shape?

After:
1. **Does it exist?**: Did I actually produce a list with categories and items? Is anything missing?
```

**Fix 5** — Hide system IDs from the learner-facing metadata. Move them to a comment or the footer only:
```
Before:
> **Source**: RIU-401 | Knowledge: LIB-045, LIB-067

After:
> **Based on**: Palette Knowledge Library
```
Keep the full IDs in the footer for system traceability.

**Fix 6** — Add a note about paste length:
```
(Don't worry — it's a long paste. That's normal. The AI reads the whole thing and then starts guiding you.)
```

---

## Persona 2: Mid-Level Developer

*Uses Claude daily. Has built RAG pipelines. Wants to skip to Applied or Production. Will be annoyed if patronized.*

### What works well

- The three-tier structure respects their time. They can see Quick Start is beneath them and jump straight to Applied.
- Applied's stress test ("Pick 10 random things from your actual work. Try to classify each one.") is genuinely useful — this is how you validate a taxonomy, and even experienced devs skip this step.
- Production level is legitimately challenging. The 80% AI classification accuracy target is a real bar. The transfer test ("Could I apply this same pattern to a completely different domain?") tests actual understanding.
- The teaching rules include "If I'm moving fast, skip the basics and go deeper" — this is the right adaptive behavior for a developer who doesn't need hand-holding.
- Failure modes at Production level are real engineering concerns (inconsistent ID schemes, no escape hatch for unclassifiable inputs).

### What's confusing or would break the flow

**1. Applied doesn't explicitly say "you can skip Quick Start."**
The levels are presented sequentially. A developer scanning the document sees Quick Start first and might think it's a prerequisite. The LLM asks "which level do you want" — but only after the learner has already read through Quick Start. The skip-ahead affordance needs to be earlier and more explicit.

**2. Production assumes YAML output.**
"Write it as YAML" is baked into the Production steps. A developer building for a different system might want JSON, a database schema, or a Python dict. The format should be a choice, not an assumption. YAML is fine as the default, but the rigidity feels like a Palette-specific choice leaking into a general-purpose skill.

**3. The "AFTER YOU BUILD" sequence feels mandatory and bureaucratic.**
A developer who just built a production taxonomy doesn't want to rate their confidence on a 1-5 scale. They know what they learned. The confidence delta is valuable for beginners (it makes invisible progress visible) but feels patronizing for someone who just wrote a YAML taxonomy with routing logic. The instruction "Don't skip it" makes it worse — it removes agency.

**4. "Reasoning check" at Quick Start is too light for a developer who chose Applied.**
If a developer starts at Applied, the verification is appropriately rigorous. But if they did Quick Start first (maybe to warm up), the verification question "Why did you organize it that way?" is trivially easy for them. The skill doesn't adapt verification difficulty to the learner's apparent level — only to the chosen tier.

**5. The constellation routing assumes linear progression.**
"Organize → Retrieve → Route (1 of 3)" implies you must do taxonomy before knowledge library before multi-agent routing. A developer who already has a knowledge library might want to jump to routing. The constellation is presented as a sequence, not a menu.

### Specific suggested fixes

**Fix 1** — Add skip-ahead language before the difficulty levels:
```
Before:
Ask me which level I want. Briefly explain what each one produces so I can choose.

After:
Ask me which level I want. Each level is self-contained — you can start at any one. Briefly explain what each produces so I can choose.
```

**Fix 2** — Make Production format flexible:
```
Before (Production step 5):
5. Test with AI: give me 15 inputs from your domain.

After (add before step 2):
2. Choose your output format: YAML (default), JSON, or describe your target system and we'll match it.
```
Then adjust step references from "YAML taxonomy" to "your taxonomy."

**Fix 3** — Make AFTER YOU BUILD adaptive:
```
Before:
After I finish any level, walk me through this sequence. Don't skip it.

After:
After I finish any level, walk me through this sequence. If I want to skip a step, that's fine — but at minimum do Step 1 (confidence delta) and Step 3 (capture what you built).
```

**Fix 4** — Add a note in the constellation section:
```
Before:
⚡ YOU ARE HERE → Taxonomy Design
🔨 Next → Building a Knowledge Library
🏗️ Then → Multi-Agent Routing

After:
⚡ YOU ARE HERE → Taxonomy Design
🔨 Next → Building a Knowledge Library (or skip ahead if you already have one)
🏗️ Then → Multi-Agent Routing
```

---

## Persona 3: Educator Trying Creator Mode

*A DevRel lead who wants to create a learning path for their team. Not deeply technical. Evaluates tools on "can I use this without an engineer?"*

### What works well

- The 8 questions are asked one at a time ("Don't dump them all at once") — this is critical for non-technical users who would be overwhelmed by all 8 at once.
- Question 4 ("What's a concrete example everyone can relate to?") with the cooking/closet/road trip examples is excellent guidance. It tells the educator exactly what "universal" means.
- The quality bar checklist is actionable. "Quick Start finishes in 5 minutes with a real artifact in hand" — an educator can evaluate that.
- The post-generation review questions are the right ones. "Does the Quick Start example feel universal enough?" is exactly what an educator should be checking.
- Creator Mode is genuinely self-contained. You don't need to have used Learner Mode first to understand what you're creating.

### What's confusing or would break the flow

**1. Question 8 asks about "constellations" with insufficient context.**
> "What constellation does this belong to? (A 3-step learning arc with a name. Example: 'Prompt → Guardrail → Monitor')"

An educator who has never seen the Palette system doesn't know what a constellation is in this context. The parenthetical helps, but "3-step learning arc with a name" is still abstract. They'd likely say "I don't know" or make something up that doesn't fit the pattern. The fallback ("If you're not sure, I'll suggest one") is good but should be the default, not the fallback.

**2. Question 2 is hard to answer without understanding the three-tier framework.**
> "What should the learner BUILD at each level?"

An educator who hasn't internalized Quick Start / Applied / Production doesn't know what's appropriate at each level. They might say "a report" for all three. The question needs more scaffolding — examples of what "Quick Start output" vs "Production output" means in terms of complexity and time.

**3. The quality bar item "Works identically in ANY AI tool — no tool-specific features" is confusing.**
An educator doesn't know what "tool-specific features" means. Claude's artifacts? ChatGPT's code interpreter? Canvas? They don't know what to avoid because they don't know what the differences are. This item needs to be rephrased as a positive ("uses only plain text conversation") rather than a negative ("no tool-specific features").

**4. The generated path would feel too Palette-branded.**
The footer says "This path was generated by the Palette content engine" and links to `github.com/pretendhome/palette`. An educator creating a path for their team doesn't want Palette branding on their deliverable. They want it to feel like THEIR path. The branding should be optional or in a comment, not in the learner-facing output.

**5. The wire contract section is visible to the educator.**
The WIRE CONTRACT and PARAMETER REFERENCE sections at the bottom of the file are system internals. If an educator is reading the full document to understand Creator Mode, they'll hit these sections and think "this is too technical for me." These should be in a separate file or clearly marked as "system internals — skip this."

**6. Review question 5 ("Is the constellation arc right?") assumes they understood question 8.**
If they struggled with the constellation concept in question 8, they can't meaningfully evaluate it in the review. The review should acknowledge this: "If you skipped the constellation question earlier, skip this one too."

### Specific suggested fixes

**Fix 1** — Reframe question 8 with the fallback as default:
```
Before:
8. **What constellation does this belong to?** (A 3-step learning arc with a name...)

After:
8. **What comes before and after this skill?** (What should someone learn BEFORE this to be ready? What should they learn AFTER to go deeper? I'll organize these into a learning arc for you.)
```

**Fix 2** — Add scaffolding to question 2:
```
Before:
2. **What should the learner BUILD at each level?**

After:
2. **What should the learner BUILD at each level?**
   - Quick Start (5 min): something simple anyone could finish — like a first draft, a basic version, a starter template
   - Applied (15-30 min): something they'd use at work tomorrow — real data, real context
   - Production (30-60 min): something they'd put in a portfolio or present to their team
```

**Fix 3** — Rephrase the tool-agnostic quality bar item:
```
Before:
- Works identically in ANY AI tool — no tool-specific features

After:
- Works in any AI tool — uses only plain text conversation (no special features like file upload, code execution, or canvas)
```

**Fix 4** — Make Palette branding optional in generated paths:
```
Before:
*This path was generated by the Palette content engine.*

After:
*[Optional — remove this line if publishing under your own brand]*
*Built with the Palette content engine (github.com/pretendhome/palette)*
```

**Fix 5** — Add a section divider before the wire contract:
```
---
## SYSTEM INTERNALS (skip this — it's for the content engine, not for creators)
---
```

**Fix 6** — Make review question 5 conditional:
```
Before:
5. "Is the constellation arc right, or should this connect differently?"

After:
5. "Does the learning sequence make sense? (If we skipped the 'what comes before/after' question, we can figure this out now.)"
```

---

## Cross-Persona Issues

### What works across all personas

- The three-tier difficulty model is universally understood. Everyone gets "easy / medium / hard."
- The teaching rules ("wait for me to try," "never say it's simple," "try a different angle") are genuinely good pedagogy. They'd improve any LLM interaction.
- The confidence baseline → delta measurement is a clever design. It makes invisible learning visible. Even if developers find it slightly bureaucratic, the data it generates is valuable for improving paths.
- Common failure modes at every level are specific and practical, not generic warnings. This is the skill's strongest design feature.

### Cross-persona friction

**1. Jargon leakage.**

| Term | Where it appears | Who it confuses |
|------|-----------------|-----------------|
| "artifact" / "artifact capture" | Verification sections, AFTER YOU BUILD | Beginners — they built a list, not an "artifact" |
| "confidence delta" | AFTER YOU BUILD step 1 | Beginners — "delta" is math/engineering jargon |
| "constellation" | Header, What's Next, Creator Mode Q8 | Beginners + Educators — Palette-specific concept |
| "wire contract" / "HandoffPacket" | Section headers, parameter reference | Educators — system internals visible in the document |
| "RIU-401" / "LIB-045" | Metadata header, footer | All non-Palette users — meaningless IDs |
| "routing" / "route" | Production steps, What's Next | Beginners — technical term used without explanation |

**Suggested fix:** Create two layers in the document. The learner-facing paste section should use zero jargon. System IDs, wire contracts, and Palette-specific terms live only in the template sections (above the paste line) and the footer.

**2. The paste boundary needs to be bulletproof.**

Right now the flow is:
```
## How to use this (instructions)
---
## ▶ START HERE — PASTE EVERYTHING BELOW INTO YOUR AI TOOL
---
(the actual prompt)
```

The problem: there are two `---` horizontal rules in a row. A beginner might copy from "How to use this" (wrong) or miss the START HERE line entirely. 

**Suggested fix:** Replace the double-rule with a single, unmissable marker:
```
## How to use this
1. Open your AI tool
2. Start a fresh chat
3. Copy everything inside the box below
4. Paste it as your first message
5. The AI will ask you a couple of questions, then guide you step by step

═══════════════════════════════════════════════════════
▶ COPY EVERYTHING BELOW THIS LINE
═══════════════════════════════════════════════════════
```

**3. Emoji as structure.**

The ⚡🔨🏗️📊🔗 emoji headers render correctly in all major LLMs and browsers. They help — they create visual anchoring for the three levels. Keep them. But test in: email clients (if paths are ever emailed), PDF export, and terminal-based tools (Cursor's chat panel renders emoji fine; some terminal LLM clients may not).

**4. The "wall of text" problem is real but manageable.**

The full paste is ~2,500 words. Tested behavior:
- ChatGPT: handles it fine, processes the full system prompt
- Claude: handles it fine
- Cursor: handles it but the chat panel makes long pastes harder to review
- Mobile: works but the paste action itself is awkward on phone

**Suggested fix:** Add a note in "How to use this":
```
(The text below is long — that's intentional. Your AI tool will read all of it and use it to guide you. Just paste the whole thing.)
```

---

## Top 3 Highest-Priority Findings

These are the issues that would lose the most learners:

1. **The copy boundary is ambiguous** — a beginner who copies from the wrong point gets a broken experience. Fix: single unmissable marker + explicit "copy from here" instruction.

2. **"Start a new conversation" is tool-specific** — the first instruction a beginner follows could fail if they don't know where the "new chat" button is in their tool. Fix: tool-aware language with examples.

3. **System jargon in learner-facing text** — "artifact," "RIU-401," "constellation," "confidence delta" all signal "this isn't for me" to non-technical users. Fix: plain language in the paste section, system terms only in template/footer.

---

## Questions for the Skill Author

1. Is the Palette branding in generated paths intentional for attribution, or would you accept making it optional? The educator persona strongly wants to publish under their own name.

2. The AFTER YOU BUILD sequence — is the confidence delta data being collected anywhere, or is it purely for the learner's benefit? If it's being collected, the mandatory nature makes sense. If it's just for the learner, making it skippable for developers would reduce friction.

3. Should the wire contract and parameter reference sections be split into a separate file (e.g., `video-enablement-wire.md`)? They're valuable for the content engine but they make the main document feel more technical than it needs to be for Creator Mode users.
