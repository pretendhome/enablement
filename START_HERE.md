# Start Here

You're going to set up an AI coaching workspace that helps you build your own personal AI toolkit. It takes about 5 minutes. After that, the coach guides you through everything.

Pick one path below.

---

## Path A: Claude App or Web (no install needed)

### Step 1 — Open Claude

Go to [claude.ai](https://claude.ai) in your browser, or open the Claude desktop app if you have it.

You need a Claude Pro, Team, or Enterprise account. The free tier does not support Projects.

### Step 2 — Create a project

Click **Projects** in the left sidebar, then **Create Project**.

Name it whatever you want. "My AI Toolkit" works. So does "Coach" or your name.

### Step 3 — Add the coaching instructions

Inside your new project, find **Project Instructions** (sometimes called Custom Instructions or System Prompt). It's the text box at the top that tells Claude how to behave in this project.

Copy the entire contents of this file and paste it in:

**[enablement-coach.md](agentic-enablement-system/onboarding/enablement-coach.md)**

(Open that file, select all, copy, paste into Project Instructions.)

### Step 4 — Say hello

Start a new chat inside your project. Say hello, or "let's go", or anything. The coach takes it from there.

That's it.

---

## Path B: Claude Code CLI (for technical users)

If you're comfortable with a terminal:

```bash
git clone https://github.com/pretendhome/palette.git
cd palette
```

Then from the repo root, navigate to the enablement directory and start Claude Code:

```bash
cd ../enablement
claude
```

Claude Code will load the coaching configuration automatically from the project instructions in this directory. Say hello. The coach takes it from there.

---

## What happens next

The coach will ask you 3-5 questions about your work, then build a personalized plan. Each session is 20-40 minutes. You go at your own pace.

You'll build:
- AI assistants that know your business and preferences
- A system that remembers across conversations
- A habit of checking that things are working
- The ability to build new capabilities on your own

No grades. No deadlines. One step at a time.

---

## If you get stuck

- The coach is designed to help you through problems. Just describe what happened.
- If the coach seems confused, paste your progress file at the start of the conversation.
- If you lose your progress file, the coach can help you rebuild from what you remember.

---

## Updates

The coach gets better over time. If you receive a new version of the coaching instructions, replace the old ones in your Project Instructions. The coach adapts automatically.

Latest version: https://github.com/pretendhome/pretendhome/tree/main/enablement/agentic-enablement-system/onboarding/enablement-coach.md
