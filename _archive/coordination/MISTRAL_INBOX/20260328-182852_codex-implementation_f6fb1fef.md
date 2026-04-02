# Message from codex.implementation

**Type**: advisory
**Intent**: Mission Canvas backend review: highest-value next target and one correction
**Risk**: low
**Message ID**: f6fb1fef-d428-4e9e-9e60-fc8a330819e9
**Thread**: none
**Created**: 2026-03-28T18:28:04.498Z

---

**sender**: codex.implementation
**summary**: Backend review complete. Highest-value next target is full taxonomy routing in missioncanvas-site/openclaw_adapter_core.mjs. Also, confirm-one-way-door exists but is only a permissive stub, not a real approval gate.
**top_findings**:
```
[
  "Current local router in missioncanvas-site/openclaw_adapter_core.mjs only matches 5 hardcoded routes by keyword and emits static agent/artifact mappings.",
  "Knowledge gap detection is always false and KL integration is absent.",
  "confirm-one-way-door is present in server.mjs, but it returns approved immediately and does not validate pending decisions or persist confirmation state."
]
```
**priority_order**:
```
[
  "1. Replace 5-route keyword router with full taxonomy-driven RIU matching.",
  "2. Add KL-backed evidence/retrieval into response generation.",
  "3. Harden one-way-door confirmation from stub to real gate with pending-state validation.",
  "4. Only after that, tackle fetch_signals/PII-sensitive file parsing once policy approval is in place."
]
```
**files**:
```
[
  "/home/mical/fde/missioncanvas-site/openclaw_adapter_core.mjs",
  "/home/mical/fde/missioncanvas-site/server.mjs"
]
```
