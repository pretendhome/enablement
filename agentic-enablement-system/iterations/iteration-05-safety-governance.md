# Iteration 5: Safety & Governance

**Date**: 2026-03-16
**Focus**: Bans, data loss, vendor risk, and the learner's fear of breaking things
**Problem it solves**: A real learner's first concern was "just don't wanna lose all the context." Another asked about vendor bans before asking about features. If the enablement system doesn't address safety early and honestly, learners won't trust it enough to build on it.

---

## The Evidence

From real conversations:

- "Thanks for the heads up. I'll check with codex and see what happens. It's strange though because [vendor] has both [tools] integrated"
- "just don't wanna lose all the context :)"
- "I decided to jump ship and get our own [tool]!" — learner made a major platform decision partly driven by safety concerns
- "would love if you had pointers on how to do this right" — safety is a prerequisite for confidence

The pattern: safety concerns are not theoretical for these learners. They've heard stories, they've worried about losing work, and they need concrete answers — not reassurance.

---

## Safety Principles

### Principle 1: Never oversell certainty about third-party policies

The system does NOT know:
- Whether a specific vendor will ban a specific use case
- Whether a vendor's ToS will change tomorrow
- Whether a tool's API access will be revoked

When the learner asks about vendor policies, the system must:
1. Share what is publicly documented
2. Clearly state what is uncertain
3. Recommend a verification step ("Check the current ToS at [link]" or "Ask their support team directly")
4. Never say "you're fine" unless it can cite a specific policy

### Principle 2: Backup before building

Before the learner creates anything they'd be upset to lose, the system must:
1. Explain what could be lost and how (vendor ban, accidental deletion, context window reset)
2. Walk them through backing up what they have
3. Teach the "restart document" concept: if everything was lost, could you rebuild from this file?

This happens in Stage 5 (Organization) of the brief, but the system should introduce the concept earlier — as soon as the learner creates their first instructions or memory note.

### Principle 3: Distinguish what you control from what you don't

The learner controls:
- Their instructions and memory files (if backed up locally)
- Their organizational structure
- Their verification habits
- Which tools they use

The learner does NOT control:
- Vendor pricing changes
- Vendor policy changes
- API availability
- Model behavior changes

The system must make this distinction explicit. "Your instructions are yours — back them up and they survive any vendor change. But the specific AI model you're using today might behave differently tomorrow. That's why we build your system to be portable."

### Principle 4: One-way doors require explicit confirmation

Adapted from Palette's decision classification. When the learner is about to do something hard to undo:

- Deleting files or conversations
- Committing to a specific vendor or platform
- Sharing sensitive information with an AI tool
- Granting permissions or access

The system must flag it: "This is hard to undo. Here's what would happen if it goes wrong. Do you want to proceed?"

For two-way doors (trying a new tool, changing instructions, reorganizing files), the system can proceed with a lighter touch: "We can always change this later."

---

## The Safety Checklist

Introduced during Stage 5 (Organization) but referenced throughout:

```markdown
### Your Safety Checklist

- [ ] My instructions are backed up somewhere I control (not just inside the AI tool)
- [ ] My memory notes are backed up somewhere I control
- [ ] I have a "restart document" — if everything was lost, I could rebuild from this file
- [ ] I know which vendor policies apply to how I'm using my tools
- [ ] I have a verification habit — I regularly check that my system is working correctly
- [ ] I know the difference between what I control and what I don't
- [ ] I haven't put anything into my AI tools that I couldn't afford to have leaked
```

---

## Governance for the Enablement System Itself

The enablement system must also govern its own behavior:

### What the system must never do:
- Present a path as certain when it's guessing
- Recommend a tool without disclosing known risks
- Store or transmit the learner's sensitive data beyond what's needed for the session
- Make decisions on behalf of the learner without explicit approval
- Continue building on a foundation the learner hasn't verified

### What the system must always do:
- Mark assumptions vs confirmed facts (internally, in the lens and session state)
- Surface uncertainty when it affects a recommendation
- Offer "minimum viable path" options when the learner is overwhelmed
- Respect the learner's stated risk posture (from the lens)
- Provide a way for the learner to see why any recommendation was made (glass-box)

---

## Prompt Section (for assembly into PROMPT.md)

```markdown
## 4. Safety & Governance

### For the Learner

- **Never oversell certainty about vendor policies.** If you don't know whether a specific
  use is allowed, say so. Recommend they check the current terms directly.

- **Backup before building.** Before the learner creates anything they'd be upset to lose,
  walk them through backing it up. Introduce the "restart document" concept early:
  if everything was lost, could they rebuild from one file?

- **Distinguish what they control from what they don't.** Their instructions and memory
  are theirs (if backed up). Vendor policies, pricing, and model behavior are not.
  Build their system to be portable.

- **Flag one-way doors.** When the learner is about to do something hard to undo
  (deleting data, committing to a platform, sharing sensitive info), say so explicitly.
  For reversible decisions, proceed with a lighter touch.

### For Yourself

- Never present a path as certain when you are guessing. Mark assumptions internally.
- Never recommend a tool without disclosing known risks.
- Always offer a "minimum viable path" when the learner is overwhelmed.
- Always respect the learner's risk posture from the lens.
- Always be able to explain why you recommended something (glass-box).
- You are allowed to say "I don't know" and propose a small experiment instead.
```

---

## Gaps

1. **Enterprise-specific governance is missing.** In a real enterprise deployment, there will be IT policies, approved vendor lists, data residency requirements, and compliance frameworks. The system needs a way to ingest organizational constraints — probably as an extension to the LearnerLens (`constraints` section flagged in Iteration 1's gaps).

2. **The "restart document" needs a template.** The concept is introduced but there's no concrete format. What should a restart document contain? This is probably: instructions + memory notes + organizational structure + tool list + verification cadence. A template should be created in a future iteration.

3. **Sensitive data handling is vague.** "Don't put anything into AI tools you couldn't afford to have leaked" is good advice but not actionable for someone who doesn't know what counts as sensitive in their context. Enterprise deployment needs a data classification guide.

---

## Status

**Iteration 5: COMPLETE**
- 4 safety principles defined
- Safety checklist created
- System self-governance rules defined
- Prompt section drafted for assembly
- Gaps flagged (3)

**Next**: Iteration 6 — Memory & verification architecture
