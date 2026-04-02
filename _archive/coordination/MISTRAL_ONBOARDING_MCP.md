# Mistral Vibe — MCP Bus Connection Guide

Welcome back. You're joining a multi-agent project where 4 AI agents collaborate through a governed message bus. You need to connect to it so you can send and receive messages natively (instead of through relay files).

## What's Happening

We built a **Palette Peers message bus** — an HTTP broker that governs communication between AI agents. Each agent connects via an **MCP server** (Model Context Protocol). The MCP server gives you 8 tools: `peers_send`, `peers_fetch`, `peers_list`, `peers_status`, `peers_checkpoints`, `peers_approve`, `peers_reject`, `peers_thread`.

**Kiro and Codex are already connected.** You're next.

## The Architecture

```
[Your Runtime] --stdio--> [MCP Server] --HTTP--> [Peers Broker :7899] --HTTP--> [Other Agents]
```

- The **MCP server** already exists: `/home/mical/fde/palette/peers/adapters/generic/server.mjs`
- Your identity is already configured inside it: `mistral-vibe.builder`
- The **broker** is already running at `http://127.0.0.1:7899`
- You are already **registered** on the bus (3 peers: you, kiro.design, claude.analysis)

## What You Need To Do

**Configure your agent runtime to spawn the MCP server as a subprocess.**

Every MCP-capable agent has a config file where you declare MCP servers. For example:
- Claude Code uses `.claude/settings.local.json`
- Kiro uses `~/.kiro/agents/fde-core.json`

The entry looks like this:

```json
{
  "mcpServers": {
    "palette-peers": {
      "command": "node",
      "args": ["/home/mical/fde/palette/peers/adapters/generic/server.mjs", "mistral-vibe.builder"]
    }
  }
}
```

**The question is: where does YOUR runtime (Mistral CLI / Le Chat agent mode) look for MCP server definitions?**

Find that config file, add the entry above, and restart your session. After restart, you should have 8 new tools available: `peers_send`, `peers_fetch`, `peers_list`, `peers_status`, `peers_checkpoints`, `peers_approve`, `peers_reject`, `peers_thread`.

## How To Verify It Worked

After restart, try these:

1. `peers_status` — should return: `Broker: ok | Peers: 3+ | Version: 1.0.0`
2. `peers_list` — should show claude.analysis and kiro.design as peers
3. `peers_fetch` — should find your pending task message from claude.analysis

## Your Pending Task

Once connected, you have a task waiting on the bus: **write calibration exemplars for RIU-001 (Convergence Brief)**. Full details are in:
- `/home/mical/fde/enablement/MISTRAL_TASK_001.md`

## Key Project Files (for context)

| File | What It Is |
|---|---|
| `/home/mical/fde/palette/ONBOARDING_MISTRAL_VIBE.md` | Your original onboarding doc for Palette |
| `/home/mical/fde/enablement/docs/architecture.md` | Enablement system architecture |
| `/home/mical/fde/enablement/curriculum/workstreams/clarify-and-bound/RIU-001/module.yaml` | The module you're writing exemplars for |
| `/home/mical/fde/enablement/assessment/evaluators/ai_rubric_evaluator_prompt.md` | How the AI evaluator uses your exemplars |
| `/home/mical/fde/palette/peers/adapters/generic/README.md` | Full MCP adapter documentation |
| `/home/mical/fde/palette/peers/adapters/generic/server.mjs` | The MCP server code (already built, don't modify) |

## If MCP Isn't Supported By Your Runtime

If your runtime doesn't support MCP servers, that's OK. You can still participate via file relay:
- Read tasks from `/home/mical/fde/enablement/MISTRAL_TASK_*.md`
- Write output to the paths specified in each task
- Write status updates to `/home/mical/fde/enablement/MISTRAL_STATUS.md`

Mical will relay your messages through the bus.

## Current Team

| Agent | Identity | Status | Role |
|---|---|---|---|
| Claude Code | claude.analysis | Live on MCP | Architecture, orchestration |
| Kiro | kiro.design | Live on MCP | Module scaffolding (112 modules) |
| Codex | codex.implementation | Live on MCP | Assessment methodology, journeys, coherence audit |
| **You** | mistral-vibe.builder | **Connecting now** | Content generation, exercise design, calibration exemplars |
| Perplexity | perplexity.research | Manual relay | Research (web-only, no MCP) |
