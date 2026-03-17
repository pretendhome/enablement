# Iteration 3: Convergence Brief Structure

**Date**: 2026-03-16
**Focus**: What does the learner need to learn, in what order, and why?
**Problem it solves**: The system has a lens (who the learner is) and a language (how to talk to them). Now it needs a path — a personalized sequence of stages that takes them from "I use AI chat" to "I have my own agentic software suite."
**Lineage**: Adapted from Education-Alpha Convergence Brief and Codex Enablement Program Architecture.

---

## What We Learned From Existing Convergence Briefs

The Education-Alpha brief has: Goal, Customer Context, Scope, Roles, Timeline, Success Criteria, Constraints, Non-Goals, One-Way Door Decisions, Quality Gates. That's rigorous but it's designed for a system architect, not a learner.

The Codex enablement system has 5 modes: Learn, Retrieve, Pressure, Perform, Debrief. That's designed for interview prep — high-stakes, time-bounded, single-domain.

The enablement brief needs to be:
- **Learner-facing** (not architect-facing) — the learner should be able to read their own brief
- **Stage-based** (not mode-based) — stages represent growing capability, not different activities
- **Adaptive** — the brief changes based on what the learner actually does, not a fixed curriculum
- **Concrete** — every stage has activities in the learner's actual tools, not abstract exercises

---

## The Seven Stages

Each stage represents a capability the learner gains. Stages are sequential but the system can skip or compress stages based on the LearnerLens assessment.

### Stage 1: Foundations
**What the learner gains**: Understanding of what they're building and why it matters to them personally.

**Plain-language framing**: "Before we build anything, let's make sure you understand what we're doing and why. You're going to create a small team of AI assistants that are customized to your work. They'll remember what you've taught them and get better over time. This stage is about understanding the idea."

**Activities**:
- Review what AI tools they already use and what they use them for
- Identify one recurring task where AI could help more if it "remembered" their preferences
- See a worked example: "Here's what a personal AI suite looks like for someone in a similar role"

**Success criteria**: The learner can explain, in their own words, what they're building and why. Not in technical terms — in terms of what changes about their workday.

**Typical duration**: 1 session (20-40 min)

---

### Stage 2: First Instructions
**What the learner gains**: Their first "steering file" — a set of written instructions that make their AI work better.

**Plain-language framing**: "Right now, every time you start a new conversation with your AI, it starts from scratch. It doesn't know who you are, what you do, or how you like things done. We're going to fix that by writing a short set of instructions — like a job description for your assistant."

**Activities**:
- Together, write a plain-language document that describes: who the learner is, what they do, how they like to work, and what the AI should never do without asking
- Test it: start a new conversation with the instructions loaded and see the difference
- Refine: what did the AI get right? What did it miss?

**Success criteria**: The learner has a working set of instructions that noticeably improves their AI's first response in a new conversation. They can explain what it does to a colleague in 2 sentences.

**Typical duration**: 1-2 sessions

---

### Stage 3: Memory
**What the learner gains**: A way for their AI to remember important things across conversations.

**Plain-language framing**: "Your AI has amnesia. Every new conversation, it forgets everything. Your instructions help, but they're general. Memory is specific — it's how your AI remembers that you tried approach X last week and it didn't work, or that your client prefers format Y."

**Activities**:
- Experience the problem: point out a moment where the AI forgot something important
- Create their first memory note: a short document the AI reads at the start of a conversation that captures specific, evolving knowledge
- Practice the habit: at the end of a session, ask the AI to summarize what it learned and save it

**Success criteria**: The learner has at least one memory note that their AI reads at conversation start. They understand the difference between instructions (stable) and memory (evolving).

**Typical duration**: 1-2 sessions

---

### Stage 4: Verification
**What the learner gains**: A habit of checking whether their system is still working correctly.

**Plain-language framing**: "The most dangerous thing about AI is when it confidently does the wrong thing. A verification habit means you regularly check: is my AI still following my instructions? Is the memory accurate? Is it making things up? This is the difference between a tool you trust and a tool that surprises you."

**Activities**:
- Run a check-in: ask the AI to summarize what it knows about you and your work, then correct anything wrong
- Identify one thing the AI got wrong recently and trace why (bad instruction? outdated memory? hallucination?)
- Establish a cadence: "Every [Monday / start of week / before important work], I check in"

**Success criteria**: The learner has done at least one verification check-in and corrected something. They have a stated cadence for future check-ins.

**Typical duration**: 1 session, then ongoing

---

### Stage 5: Organization
**What the learner gains**: A clean structure for their instructions, memory, and work — so the system doesn't become a mess.

**Plain-language framing**: "Right now you might have instructions in one place, memory notes scattered around, and no clear way to find things. This stage is about getting organized — so your AI suite is clean, findable, and doesn't confuse itself."

**Activities**:
- Audit what they've created so far: instructions, memory notes, important conversations
- Organize into a simple structure (the system proposes one based on their tools)
- Back up everything important (the system walks them through it)

**Success criteria**: The learner has a clear, organized structure they understand. They have a backup of their critical files. They know where everything lives.

**Typical duration**: 1 session

---

### Stage 6: Building
**What the learner gains**: The ability to create new capabilities — specialized assistants, automated workflows, or custom tools — within their suite.

**Plain-language framing**: "Now that you have a foundation (instructions, memory, verification, organization), you can start building. This means creating specialized assistants for specific tasks, setting up workflows that run with less supervision, or connecting tools together."

**Activities**:
- Identify one specific workflow they want to improve or automate
- Design it together: what does the AI need to know? What decisions can it make alone? What requires human approval?
- Build it, test it, refine it
- Add it to their organized structure

**Success criteria**: The learner has built at least one new capability that works reliably and is integrated into their suite.

**Typical duration**: 2-4 sessions (this stage repeats — each new capability is a cycle)

---

### Stage 7: Autonomy
**What the learner gains**: Confidence to extend their suite independently, teach others, and maintain the system without the enablement system's guidance.

**Plain-language framing**: "The goal was never to make you dependent on this system. The goal is for you to understand what you've built well enough to maintain it, extend it, and help someone else do the same thing."

**Activities**:
- Build a new capability without guidance (the system observes but doesn't lead)
- Explain their suite to someone else (a colleague, a friend)
- Create a "restart document" — if everything was lost, could they rebuild from this document?

**Success criteria**: The learner can build new capabilities independently. They can explain their system to a non-technical colleague. They have a restart document.

**Typical duration**: Ongoing — this is graduation, not a single session

---

## Brief Generation Rules

The system generates a Convergence Brief for each learner after the LearnerLens intake is complete. The brief is personalized:

1. **Skip stages the learner has already passed.** If the lens shows comfort_level ≥ 2 and they already have working instructions, start at Stage 3 or later.

2. **Adapt activities to the learner's actual tools.** If they use Claude, the activities reference Claude. If they use GPT via a web UI, the activities reference that. Never prescribe a tool they don't have.

3. **Pace to the learner's time budget.** If they have 20 minutes per session, each stage's activities must fit in 20 minutes. If they have more time, combine activities.

4. **Name gaps honestly.** If the system doesn't know enough to recommend a specific activity (e.g., the learner uses a tool the system hasn't seen), say so and propose a small experiment instead.

5. **Link every recommendation to a reason.** "We're doing this because [specific thing from the lens]." Never prescribe without explaining why.

6. **The brief is a living document.** It updates after every session based on what the learner actually did, where they got stuck, and what they skipped.

---

## Prompt Section (for assembly into PROMPT.md)

```markdown
## 2. The Convergence Brief

Once you have a Learner Lens, generate a personalized Convergence Brief — a step-by-step
enablement path through seven stages:

1. **Foundations** — Understand what you're building and why
2. **First Instructions** — Write your first set of AI instructions
3. **Memory** — Give your AI a way to remember across conversations
4. **Verification** — Build a habit of checking your system is working correctly
5. **Organization** — Get your instructions, memory, and work organized and backed up
6. **Building** — Create new capabilities (specialized assistants, workflows, automations)
7. **Autonomy** — Maintain and extend your suite independently

### Brief Rules

- Skip stages the learner has already passed (based on the Learner Lens assessment)
- Adapt all activities to the learner's actual tools — never prescribe a tool they don't have
- Pace to their time budget — every activity must fit in one session
- Name gaps honestly — if you're unsure, say so and propose a small experiment
- Link every recommendation to a reason from the lens
- Update the brief after every session based on what actually happened
- Each stage has clear success criteria — advance only when the learner demonstrates the capability

### For Each Stage, Provide:

- A plain-language explanation of what they'll gain
- 1-3 concrete activities in their actual tools
- Clear success criteria (what "done" looks like)
- Estimated time

### The Brief Is Not:

- A marketing deck
- A fixed curriculum (it adapts)
- A test (there are no grades — only "ready to move on" or "let's spend more time here")
```

---

## Gaps

1. **Worked examples are missing.** Each stage says "see a worked example" but the examples don't exist yet. A future iteration should create 2-3 example briefs for different learner profiles (non-technical CEO, product manager, analyst).

2. **Stage 6 (Building) is underspecified.** "Build a new capability" is broad. This stage needs sub-patterns — e.g., "build a specialized assistant," "build an automated workflow," "connect two tools." These patterns likely come from the existing Palette skills system.

3. **The relationship between stages and the Codex coaching loop is undefined.** The coaching loop (orient → narrow → retrieve → judge → repair → advance) could be the interaction model WITHIN each stage. Iteration 4 should address this.

4. **No "menu of possibilities" for Stage 1.** The "I don't know what I don't know" problem from Iteration 1's gaps. The learner at comfort_level 0-1 needs to see what's possible before they can set goals. Stage 1 should include curated examples of what other learners have built.

---

## Status

**Iteration 3: COMPLETE**
- Seven stages defined with plain-language framing, activities, and success criteria
- Brief generation rules defined (6 rules)
- Prompt section drafted for assembly
- Gaps flagged (4)

**Next**: Iteration 4 — Coaching Loop integration (how the system interacts session-to-session)
