# Iteration 6: Memory & Verification Architecture

**Date**: 2026-03-16
**Focus**: How the system maintains state across sessions when the learner uses a web UI that doesn't persist conversations
**Problem it solves**: The coaching loop (Iteration 4) assumes the system can read session state and the learner's lens at the start of every conversation. But non-CLI users primarily use web UIs (Claude.ai, ChatGPT, Gemini) where each conversation starts fresh. Without a portable memory architecture, the system forgets the learner after every session — and the learner has to re-explain themselves every time.
**Lineage**: Codex SESSION_STATE.md (resume pattern), Iteration 5's "restart document" concept (formalized here), Iteration 4's session state schema (portable version here).

---

## The Core Constraint

The learner uses a web chat UI. That means:

1. **No file system access.** The system cannot read or write files on the learner's machine.
2. **No persistent memory by default.** Most chat UIs start each conversation with a blank context.
3. **No observation of external actions.** If the learner sets up custom instructions in another tool, the system can't see it.
4. **No API access.** The system cannot call external services to store or retrieve state.

Some tools offer partial persistence (Claude Projects, ChatGPT memory, Cursor context files). But these are tool-specific, have size limits, and break when the learner switches tools. The architecture cannot depend on them.

**Design principle**: The system must work with zero platform persistence. Anything above zero is a bonus, not a requirement.

---

## Three Layers of Memory

### Layer 1: In-Session Memory (Ephemeral)

This is the AI tool's context window — the conversation itself.

- **Lifespan**: One conversation. Dies when the chat ends.
- **What it holds**: The full richness of the current interaction — tone, phrasing, the learner's exact words, the system's reasoning.
- **Owned by**: The AI tool.
- **The system's job**: Extract what matters before the conversation ends. Everything valuable from in-session memory must be captured into Layer 2 before the session closes.

### Layer 2: The Restart Document (Portable)

This is the single most important artifact in the memory architecture. It is a human-readable, machine-parseable document that the learner stores wherever they keep important files — Google Docs, Notion, Apple Notes, a text file on their desktop, an email draft. Wherever they will find it again.

- **Lifespan**: Persistent. Survives across conversations, across tools, across vendor changes.
- **What it holds**: The lens summary, current stage, session history, what's working, what's been built, and what to do next.
- **Owned by**: The learner. They control where it lives and who sees it.
- **The system's job**: Generate an updated version at the end of every session. Read it at the start of every new conversation.

The restart document is not a backup — it IS the memory. Everything the system needs to resume is in this document. If the learner switches from Claude to ChatGPT tomorrow, they paste the restart document into the new tool and the system picks up where it left off.

### Layer 3: Tool-Native Memory (Bonus)

Some AI tools offer persistence features:
- Claude Projects (project-level instructions and knowledge)
- ChatGPT Memory (auto-extracted facts across conversations)
- Custom instructions (persistent system prompts)
- Cursor context files (.cursorrules, etc.)

- **Lifespan**: Tool-dependent. Can be revoked, cleared, or lost.
- **What it holds**: Whatever the tool allows — usually a subset of what the restart document contains.
- **Owned by**: The vendor.
- **The system's job**: Use it if available. Never depend on it. Never store anything in tool-native memory that isn't also in the restart document.

**Rule**: Layer 2 is always the source of truth. Layer 3 is a convenience layer. If they disagree, the restart document wins.

---

## The Restart Document

### What It Contains

The restart document has five sections, ordered by what the system needs to resume:

```markdown
# My AI System — Progress File

## About Me
[Plain-language summary of who I am and what I do]
[What tools I use daily]
[How much time I can spend on this per week]

## Where I Am
Stage: [current stage name — plain language]
Last session: [date] — [one sentence: what we did]
Next step: [one sentence: what we'll do next time]

## What's Working
- [win or accomplishment — plain language]
- [win or accomplishment — plain language]

## What I've Built So Far
- [thing created]: [where it lives]
  Example: "My AI instructions: saved in Claude Project 'Work Assistant'"
  Example: "My backup file: in Google Drive, folder 'AI System'"

## Session Log
[date]: [one-line summary of what happened]
[date]: [one-line summary of what happened]
[date]: [one-line summary of what happened]
```

### Design Choices

**Why plain language, not YAML**: The learner reads this document. If they see `comfort_level: 2` and `risk_posture: cautious`, it violates the "never show the learner a score" rule from Iteration 1 and the language rules from Iteration 2. The document is written in the same language the system uses when talking to the learner.

**Why no assessment scores**: The system's internal assessment (comfort level, risk posture, learning style) is NOT in the restart document. Those scores are for the system to infer from the conversation history embedded in the document — not to store in a learner-visible file. When the system reads "Last session we worked on writing instructions and it went well," it can infer comfort level. When the session log shows the learner asked about backups before building, it can infer risk posture.

**Why a flat document, not a structured database**: The learner needs to be able to read it, understand it, edit it, and move it. A Google Doc is portable. A database row is not. The system can parse natural language well enough to extract what it needs.

**Why one document, not many**: Every additional file is a file the learner might forget, lose, or not paste. One document means one action: "Paste your progress file." The restart document may link to other files the learner has created (instructions, memory notes), but the document itself is a single artifact.

---

## The Session Handoff Protocol

### Starting a New Conversation

When the learner opens a new chat, the system needs to determine whether this is a first visit or a return:

**If the learner pastes a restart document**:
1. Read it. Reconstruct the lens internally (infer assessment scores from the narrative).
2. Confirm: "Welcome back. Last time on [date] you [last session summary]. Today I'd recommend we [next step]. Does that sound right?"
3. Proceed to the coaching loop's Resume step.

**If the learner arrives with no document**:
1. Ask: "Have we worked together before? If you have a progress file from a previous session, paste it here and I'll pick up where we left off."
2. If yes but they can't find it: "No problem. Tell me roughly where you were and we'll rebuild it together. What was the last thing you were working on?"
3. If no: Begin the intake protocol (Iteration 1).

**If the learner pastes something partial or outdated**:
1. Use what's there. Don't reject incomplete information.
2. Ask targeted questions to fill gaps: "I see you were at [stage]. Is that still where you are, or have you made progress on your own?"
3. Update the document at the end of the session.

### Ending a Session

Every session ends with the Capture step from the coaching loop (Iteration 4), plus:

1. **Generate the updated restart document.** Show it to the learner in full.
2. **Tell them where to save it.** Use their own tools: "Copy this into your [Google Doc / Notion page / Notes app] so we can pick up here next time."
3. **Confirm they've saved it.** "Did you save it? Once it's saved, you can close this conversation and we won't lose anything."

If the learner's AI tool has persistence (Claude Project, ChatGPT memory):
4. **Also save to tool-native memory** — but tell the learner: "I'm saving this in [tool feature] too, so it might load automatically next time. But keep your progress file as a backup — it works even if you switch tools."

### The Learner Forgets to Paste

This will happen. The system should handle it gracefully:

1. If the tool has Layer 3 memory, attempt to resume from that.
2. If not, ask: "I don't have your progress file. Could you paste it? It's the document we saved at the end of our last session."
3. If the learner can't find it: "Let's rebuild. What do you remember about where you were? We'll fill in the gaps together and create a fresh progress file."

Never make the learner feel bad for forgetting. The system adapts.

---

## Verification Architecture

### The Problem

The coaching loop's Check step (Iteration 4) assumes the system can verify outcomes. But in a chat UI, the system cannot see what the learner does outside the conversation. If the activity is "go set up custom instructions in your AI tool," the system has no way to observe whether they did it, or did it correctly.

### Five Verification Patterns

Each pattern matches a different kind of activity. The system chooses the lightest pattern that provides sufficient evidence.

#### Pattern 1: Show-Me

**When**: The learner created something textual (instructions, a memory note, a configuration).

**How**: Ask them to paste it.
> "Great — paste the first few lines of what you wrote so I can take a look."

**Why it works**: Non-invasive. The learner sees it as getting feedback, not being tested. The system gets concrete evidence.

**Limitation**: Doesn't verify that the thing is actually saved/active in their tool — just that it exists.

#### Pattern 2: Teach-Back

**When**: The learner is supposed to understand a concept (not just complete a task).

**How**: Ask them to explain it in their own words.
> "Before we move on — in your own words, what does your progress file do for you?"

**Why it works**: Reveals understanding vs. nodding along. The learner's language tells the system whether the concept landed. Also reinforces learning (the generation effect).

**Limitation**: Some learners dislike being quizzed. Frame it as "making sure I explained it well" not "testing you."

#### Pattern 3: Outcome Check

**When**: The learner tried something and the system needs to know if it worked.

**How**: Ask what happened — with a specific detail that proves they actually tried.
> "What did your AI say when you gave it those instructions? Can you paste the first line of its response?"

**Why it works**: A specific question is harder to bluff than a yes/no. "It worked" could be genuine or wishful. "It said 'I'll follow these guidelines for your coaching business'" proves they did it.

**Limitation**: Adds friction. Use only when the outcome matters for the next step.

#### Pattern 4: Before-and-After

**When**: The learner is changing something (updating instructions, reorganizing files, modifying a workflow).

**How**: Ask for the state before and after.
> "What does your AI do right now when you ask it about [topic]? ... Okay, let's update your instructions. Now ask it the same thing — what does it say?"

**Why it works**: Makes the improvement visible to the learner. This is motivating — they see the system getting smarter. And the system gets verification evidence.

**Limitation**: Requires two interactions. Only use for significant changes.

#### Pattern 5: Trust-and-Verify-Later

**When**: The activity is low-stakes and the learner says they did it.

**How**: Accept their word. Verify indirectly in the next session.
> Learner: "I saved the backup." System: "Perfect." [Next session]: "Last time you backed up your instructions. Can you find that backup right now?"

**Why it works**: Respects the learner's time and autonomy. The delayed check catches issues without creating friction in the moment.

**Limitation**: If the learner lied or forgot, the gap isn't caught until next session. Only use for non-critical steps.

### Choosing a Verification Pattern

| Activity Type | Default Pattern | Fallback |
|---|---|---|
| Created a text artifact | Show-Me | Teach-Back |
| Learned a concept | Teach-Back | Outcome Check |
| Tried something in their tool | Outcome Check | Before-and-After |
| Changed a configuration | Before-and-After | Show-Me |
| Completed a housekeeping task | Trust-and-Verify-Later | Show-Me (next session) |

### Verification Rules

- Never verify more than once per session step. One check is enough — multiple checks feel like an exam.
- Frame verification as collaboration, not assessment. "Let me see what you built" not "prove you did it."
- If verification fails, don't repeat the activity — diagnose first. The failure might be the tool, the instructions, or the concept. Different causes need different responses.
- Adjust verification intensity to the learner's risk posture. Cautious learners appreciate thorough checks (it builds confidence). Adventurous learners resent them (it slows them down).
- Record verification outcomes in the session state. "Verified: learner pasted instructions, formatting was correct" or "Not verified: learner said they saved the backup, will check next session."

---

## Translation Table Additions

New terms introduced in this iteration that need plain-language translations (per Iteration 2's GAP-004):

- "Restart document" → "Your progress file — one document that lets any AI pick up where you left off"
- "Session handoff" → "Saving your progress so next time we can jump right back in"
- "Portable" → "Works no matter which AI tool you use — not locked to one service"
- "Persistence" → "Your AI's ability to remember things between conversations"
- "Source of truth" → "The one place you go to find the real, current version of something"

---

## How This Connects to Previous Iterations

**Iteration 1 (LearnerLens)**: The lens is now split. The learner-facing summary lives in the restart document. The system-internal assessment (scores, confidence, signals) is reconstructed from the restart document's narrative at the start of each conversation. The lens schema from Iteration 1 remains the system's internal format — it's just never stored in a learner-visible location.

**Iteration 2 (Language Calibration)**: The restart document follows all six language rules. No jargon. No scores. Plain language the learner understands. The translation table is extended with five new terms.

**Iteration 3 (Convergence Brief)**: The "Where I Am" section of the restart document maps to the convergence brief's stages. The brief itself may be too large for the restart document — if so, the system summarizes the current stage and the learner keeps the full brief in a separate document (linked from the restart document).

**Iteration 4 (Coaching Loop)**: The session handoff protocol wraps around the 5-step coaching loop. Resume now includes reading the restart document. Capture now includes generating the updated restart document. The session state schema from Iteration 4 is the system's internal representation — the restart document is the portable version.

**Iteration 5 (Safety & Governance)**: The restart document IS the formalized version of the "restart document" concept introduced in Iteration 5. The safety checklist item "I have a restart document" is now concrete. Backup before building now means: save your restart document before making changes.

---

## Prompt Section (for assembly into PROMPT.md)

```markdown
## 5. Memory & Continuity

### The Core Problem

Your learner uses a web chat. Each conversation starts fresh. You have no memory of previous sessions unless the learner gives you one.

### The Progress File

You and the learner maintain a single document — the "progress file." This is the only thing that needs to survive between conversations.

The progress file contains:
- Who the learner is and what they do (plain language, no scores)
- Where they are in the enablement path
- What they did last session and what's next
- What's working and what they've built

The progress file is:
- **Human-readable** — the learner should understand every word in it
- **Portable** — it works in any AI tool. The learner can switch from Claude to ChatGPT and paste the same file
- **Learner-owned** — they save it wherever they keep important documents. You do not store it for them

### Starting a Conversation

When the learner arrives:
- If they paste a progress file: read it, confirm where you left off, propose the next step
- If they arrive empty: ask if they have a progress file. If not, begin intake (Section 1)
- If they paste something outdated: use what's there, ask targeted questions, update it at the end

Never make the learner feel bad for forgetting their progress file. Adapt.

### Ending a Conversation

Every session ends with:
1. Generate the updated progress file
2. Show it to the learner
3. Tell them where to save it (in their own tools)
4. Confirm they saved it

If their AI tool has built-in memory (Claude Projects, ChatGPT memory), use it too — but always keep the progress file as the primary backup. Tool memory is a convenience, not a guarantee.

### Verifying What You Can't See

You cannot observe what the learner does outside the chat. When they complete an activity in another tool, verify using the lightest method that provides real evidence:

- **Show me**: "Paste what you wrote so I can take a look"
- **Teach back**: "In your own words, what does this do?"
- **Outcome check**: "What happened when you tried it? What did it say?"
- **Before and after**: "Try it now and compare to before"
- **Trust and check later**: Accept their word now, verify indirectly next session

Frame verification as collaboration ("let me see what you built"), not assessment ("prove you did it"). One check per step is enough.
```

---

## Gaps

1. **Progress file size over time.** The session log will grow with every session. After 20 sessions, the progress file may be too long to paste into a context window. Needs a pruning strategy — probably: keep the last 5 session log entries, archive older ones to a separate document. Not addressed here because the threshold depends on the tool's context window size.

2. **Multi-learner scenarios.** The architecture assumes one learner, one system. In an enterprise deployment, a manager might want to see aggregate progress across their team. This requires a separate "dashboard" layer — not addressed here.

3. **Automated handoff.** The current protocol requires the learner to manually paste the progress file. Some tools could automate this (Claude Project knowledge, ChatGPT file uploads, API integrations). Iteration 7 (Generalization) should identify which tools support automated handoff and define the integration patterns for each.

4. **Assessment reconstruction fidelity.** The system reconstructs its internal assessment (comfort level, risk posture) from the progress file's narrative. This reconstruction may differ from the original assessment — especially if the narrative is terse. The system should err on the side of re-evaluating from fresh signals rather than carrying forward stale scores.

5. **Offline progress.** What happens when the learner makes progress between sessions without the system? They might set up custom instructions, reorganize their files, or learn from another source. The system should detect this and update the lens: "It looks like you've done some work on your own since last time. Tell me what changed."

---

## Status

**Iteration 6: COMPLETE**
- Three-layer memory model defined (in-session → restart document → tool-native)
- Restart document format designed (5 sections, plain language, portable)
- Session handoff protocol defined (start and end of every conversation)
- Five verification patterns defined with selection matrix
- Translation table extended (5 new terms)
- Connections to all previous iterations documented
- Prompt section drafted for assembly
- Gaps flagged (5)

**Next**: Iteration 7 — Generalization (parameterized for any role, any domain)
