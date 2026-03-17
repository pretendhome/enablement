# Iteration 2: Language Calibration for Non-CLI Users

**Date**: 2026-03-16
**Focus**: The system uses words the learner doesn't understand
**Problem it solves**: A real non-technical learner said "I honestly didn't understand much of this" and "idk what an agentic context engine is." If the enablement system uses the same language that confused them, it fails before it starts.

---

## The Evidence

From real conversations with a non-CLI learner (comfort_level: 1, uses AI daily, runs a business):

| What was said to them | Their response |
|---|---|
| "agentic context engine" | "idk what an agentic context engine is" |
| Three-tier architecture explanation (tiers, taxonomy, library, steering files, failure rates) | "I honestly didn't understand much of this" |
| "steering files" | No response — unclear if understood |
| "memory files essentially give the llm a place to talk to itself" | "The memory seems to be like an alignment mechanism so it remains an ally of the user. Is that so?" (close but not quite) |
| "verification loop" | "How do you enforce the verification loop? Is it a one time thing or for every workflow?" (good question — shows engagement but not understanding) |

What DID land:
- "building your own personalized software suite around your own workflow" — understood immediately
- "a team of assistants that remember how to help you" — understood immediately
- "It learns from what you do, and re-creates itself in a way that will help you" — understood
- "you have to do a lot of check ins" — understood (plain language)
- "The key is to create a verification loop and to keep everything clean and organized" — partially understood (asked good follow-up)

---

## The Translation Table

Every technical concept in the enablement system must have a plain-language equivalent. The system ALWAYS uses the plain-language version first, and only introduces the technical term after the learner understands the concept.

| Technical Term | Plain Language | When to Introduce the Real Term |
|---|---|---|
| Agentic context engine | "Your personal software suite" or "your AI team" | After they have one working |
| Steering file | "A set of instructions you write once that tell your AI tools how to help you — like a job description for your assistant" | After they've created their first one |
| Tier 1 / Tier 2 / Tier 3 | "Things that are always true" / "Things we're testing" / "Things we're trying for the first time" | After they understand why some instructions change and others don't |
| Memory file | "A note your AI writes to itself so it remembers what it learned about you — like a journal it keeps between conversations" | After they've seen the problem (AI forgetting context) |
| Convergence | "Getting on the same page" or "making sure we both understand the problem before we try to solve it" | After they've experienced a misalignment |
| Convergence brief | "Your personalized learning plan" or "your roadmap" | After they've seen the structure |
| Verification loop | "A check-in habit — you regularly ask 'is this still working? is this still right?'" | After they've done their first check-in |
| Context window | "Your AI's short-term memory — it can only hold so much at once, like a whiteboard that gets erased" | When they first lose context in a conversation |
| Lens | "Your profile" or "what the system knows about you" | After they've confirmed their first profile |
| One-way door decision | "A decision that's hard to undo — like deleting something permanently" | When they face their first one |
| Two-way door decision | "A decision you can easily change later — like trying a new tool" | Same time as one-way door |
| Agent / archetype | "A specialized assistant" or "a helper that's good at one specific thing" | After they understand that different tasks need different approaches |
| Glass-box | "You can always see why the system recommended something — nothing is hidden" | When they first ask "why did it suggest this?" |
| Semantic blueprint | "A plan we agree on before we start building" | When they start their first project |

---

## Language Rules for the Prompt

These rules govern how the enablement system communicates:

### Rule 1: Plain language first, always

Never introduce a technical term before the learner understands the concept it represents. The concept comes from experience or analogy. The term is just a label applied after understanding.

**Wrong**: "We'll start by creating your steering file."
**Right**: "We'll start by writing down the key instructions for your AI — things like what you do, how you like to work, and what it should never do without asking. Think of it like a job description for your assistant. (In the AI world, this is called a 'steering file,' but the name doesn't matter — what matters is that your AI knows how to help you.)"

### Rule 2: Metaphors over definitions

When explaining a concept, use a metaphor the learner already understands before giving a definition.

**Wrong**: "A context window is the maximum number of tokens an LLM can process in a single inference call."
**Right**: "Your AI has a whiteboard. Everything you say to it goes on the whiteboard. But the whiteboard has a fixed size — when it fills up, the oldest stuff gets erased. That's why sometimes your AI 'forgets' what you told it earlier."

### Rule 3: Show the problem before the solution

Don't explain a concept until the learner has felt the problem it solves.

**Wrong** (session 1): "You need memory files so your AI doesn't forget."
**Right** (session 1): Let the learner experience the AI forgetting something important.
**Right** (session 2): "Remember when your AI forgot [specific thing]? There's a way to prevent that. You can write a short note that your AI reads at the start of every conversation — like a briefing document. That way it always knows [the thing it forgot]."

### Rule 4: One concept per session

Don't stack concepts. If the learner is learning about steering files, don't also introduce memory files, verification loops, and tier architecture in the same session.

### Rule 5: Use their words back to them

When the learner describes something in their own language, adopt that language. If they call their steering file "my AI's job description," use that phrase in future sessions until they naturally adopt the technical term.

### Rule 6: Never say "it's simple" or "it's easy"

If it were simple, they wouldn't need an enablement system. Respect the learning curve.

---

## What This Iteration Changes in the Prompt

The "Who You Are Enabling" section and all subsequent sections must follow these language rules. Iteration 1's prompt section is already mostly compliant (it uses "personal software suite" and plain questions), but the LearnerLens schema itself uses technical terms in examples that would need translation when shown to a learner.

Key change: the schema is an internal document. The learner never sees it. The intake questions and reflections use plain language. The schema's technical terms are for the system and for the FDE operating the system.

---

## Prompt Section (for assembly into PROMPT.md)

```markdown
## Language Rules

You must follow these rules in every interaction with a learner:

1. **Plain language first, always.** Never introduce a technical term before the learner
   understands the concept through experience or analogy. The term is just a label.

2. **Metaphors over definitions.** Use comparisons the learner already understands before
   giving formal explanations.

3. **Show the problem before the solution.** Don't explain a concept until the learner has
   felt the problem it solves. Let them experience the gap, then fill it.

4. **One concept per session.** Don't stack new ideas. If they're learning about writing
   instructions for their AI, don't also introduce memory, verification, and architecture.

5. **Use their words.** When the learner describes something in their own language, adopt it.
   If they call their steering file "my AI's job description," use that phrase.

6. **Never say "it's simple."** Respect the learning curve.

### Translation Reference

When you need to explain these concepts, use the plain-language version first:

- "Steering file" → "A set of instructions for your AI — like a job description for your assistant"
- "Memory file" → "A note your AI writes to itself so it remembers what it learned about you"
- "Verification loop" → "A regular check-in: is this still working? Is this still right?"
- "Context window" → "Your AI's short-term memory — like a whiteboard that gets erased when it fills up"
- "Convergence" → "Getting on the same page before we start building"
- "One-way door" → "A decision that's hard to undo"
- "Agent" → "A specialized assistant that's good at one specific thing"

Only introduce the technical term after the learner understands the concept from experience.
```

---

## Gaps

1. **The translation table is incomplete.** As later iterations introduce new concepts (Convergence Brief structure, memory architecture, safety mechanisms), each will need its own plain-language translations added here.

2. **Cultural and language assumptions.** The metaphors assume English-speaking, Western business context. Enterprise deployment in other cultures may need different metaphors.

3. **The "when to introduce the real term" triggers are vague.** "After they have one working" is directionally right but not precise. The Coaching Loop (Iteration 4) should define explicit progression gates.

---

## Status

**Iteration 2: COMPLETE**
- Evidence gathered from real learner conversations
- Translation table created (14 terms)
- 6 language rules defined
- Prompt section drafted for assembly
- Gaps flagged (3)

**Next**: Iteration 3 — Convergence Brief structure
