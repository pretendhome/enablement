# Codex Enterprise Enablement

Sales enablement package for deploying Codex at a Fortune 500 retail company.

## Quick Setup

```bash
git clone git@github.com:pretendhome/enablement.git
cd enablement/codex
pip install -r requirements.txt
```

## Demo Surfaces

The recording uses four surfaces:

| # | Surface | What |
|---|---------|------|
| 1 | Slide deck | `codex_enablement_v2.pptx` — open in Keynote/PowerPoint |
| 2 | Codex app | Desktop app pointed at the demo repo (see below) |
| 3 | Dashboard | `http://localhost:8501/visibility.html` |
| 4 | Loom | Recording app |

## Dashboard

Two options — use either one:

**Option A: Static HTML (recommended for recording)**
```bash
cd dashboard
python3 -m http.server 8501
# Open http://localhost:8501/visibility.html
```
Zero dependencies beyond a browser. Dark theme, embedded data, interactive queries.

**Option B: Streamlit (full interactive)**
```bash
streamlit run dashboard/app.py
# Opens http://localhost:8501
```
Requires `streamlit`, `pandas`, `plotly`. Full sidebar filters, richer visualizations.

## Demo Repo Setup

The Codex demo section requires a real Java codebase loaded in the Codex app. The script assumes a retail/POS domain.

**Recommended: JavaPOS (open-source Java POS API)**
```bash
git clone https://github.com/JavaPOSWorkingGroup/javapos-contracts.git
```

**Alternative: any substantial Java codebase with:**
- Multiple packages/modules
- Controller/Service/Repository patterns
- Configuration files
- Enough structure for architecture explanation

**Before recording:**
1. Clone the demo repo to a separate directory
2. Open it in the Codex desktop app (not the monorepo)
3. Run both prompts and note which files Codex references
4. Use those file names in your narration

### Demo Prompts

**Move 1 — Code Understanding:**
```
Explain the device management architecture in this codebase.
What are the main components, how do they interact, and what
would a new developer need to understand first?
```

**Move 2 — Limitations:**
```
What are you likely to get wrong about this codebase?
What should I verify before trusting your analysis?
```

If the demo repo doesn't have "device management," adapt the prompt:
```
Explain the architecture of this codebase. What are the main
components, how do they interact, and what would a new developer
need to understand first?
```

## Regenerating the Deck

```bash
python3 generate_deck_v2.py
# Outputs: codex_enablement_v2.pptx
```

## Files

| File | Purpose |
|------|---------|
| `codex_enablement_v2.pptx` | 7-slide presentation deck |
| `generate_deck_v2.py` | Deck generator (python-pptx) |
| `speaker_script_v2.md` | 5-minute Loom recording script |
| `speaker_script_20min_v2.md` | 20-minute live presentation script |
| `demo_runbook_v2.md` | Demo prompts, narration, contingencies |
| `defense_notes_v2.md` | Q&A prep for VP Engineering role-play |
| `loom_checklist.md` | Pre-recording and post-recording checklist |
| `dashboard/visibility.html` | Static HTML dashboard (recommended) |
| `dashboard/app.py` | Streamlit dashboard (alternative) |
| `dashboard/data/codex_usage.json` | Simulated pilot data (530 queries) |
| `requirements.txt` | Python dependencies |

## Pre-Recording Checklist

1. `git pull` — get latest changes
2. Install deps: `pip install -r requirements.txt`
3. Start dashboard: `cd dashboard && python3 -m http.server 8501`
4. Verify: `http://localhost:8501/visibility.html` loads
5. Clone demo repo and open in Codex app
6. Run both prompts to warm up Codex
7. Open deck in Keynote/PowerPoint
8. Open `speaker_script_v2.md` as reference (off-camera)
9. Disable notifications, clean desktop
10. Record
