# Learning Architecture — Portfolio Generator

Generate a visual teaching portfolio for any topic. Takes a YAML config, produces a self-contained HTML page with interactive mock previews, design philosophy, and professional presentation.

## Quick Start

```bash
# Generate a portfolio from a topic config
python3 generate.py topics/taxonomy-design.yaml

# Output: dist/taxonomy-design.html (open in browser)
```

## How It Works

1. Define a topic in `topics/` as a YAML file
2. Run the generator
3. Get a single-file HTML portfolio with:
   - Hero section with stats and positioning
   - Project showcases with mock previews
   - Design philosophy / teaching principles
   - Career timeline (optional)
   - Contact CTA

## Topic Config Format

```yaml
topic:
  id: taxonomy-design
  title: "Taxonomy Design for AI Systems"
  subtitle: "How to structure knowledge so machines and humans can navigate it"
  label: "Learning Architecture"

hero:
  headline: "Structure the knowledge right and the learning works."
  description: "A hands-on guide to designing classification taxonomies..."
  stats:
    - { num: "121", label: "RIUs Classified" }
    - { num: "47", label: "Provider Schemes Normalized" }

projects:
  - title: "Ask Pathfinder — Taxonomy Restructuring"
    label: "Case Study"
    description: "Reclassified from industry-based to function-based..."
    tags: ["Knowledge Architecture", "Retrieval", "Enterprise"]
    details:
      - heading: "Before"
        items: ["Industry-based silos", "No cross-domain transfer"]
      - heading: "After"  
        items: ["Function-based taxonomy", "Cross-domain patterns"]
    mock: dashboard  # or: oka, obsidian, enablement, custom

philosophy:
  - { title: "Classify by function, not origin", desc: "..." }
  - { title: "Human-designed signals beat automated tags", desc: "..." }

theme:
  accent: "#635bff"  # Stripe purple, or any hex
  style: light       # light or dark
```

## Available Mock Templates

| Mock ID | What it renders |
|---------|----------------|
| `oka` | Warm child-friendly learning interface with avatar, voice button, focus word |
| `dashboard` | Dark-mode data dashboard with metrics, charts, query bar |
| `obsidian` | Obsidian-style plugin with mode bar, health pills, decision cards |
| `enablement` | 3-layer assessment pipeline diagram with escalation arrows |
| `custom` | Provide your own HTML in the `mock_html` field |

## Relationship to Enablement System

Each enablement path (RIU) can have a companion portfolio page:

```
enablement/
├── paths/RIU-401-taxonomy-design.md        ← the learning path (curriculum)
├── portfolio/topics/taxonomy-design.yaml    ← the visual showcase (architecture)
├── portfolio/dist/taxonomy-design.html      ← generated output
└── video/specs/taxonomy-design-video.md     ← (future) video script
```

The three layers work together:
- **Path** teaches the competency (hands-on, paste-into-LLM)
- **Portfolio** showcases the work visually (hiring managers, demos, talks)
- **Video** walks through it on camera (YouTube, conferences)

## Design Principles

- Single-file HTML output (no dependencies beyond Google Fonts)
- Every page is a portfolio piece itself — the generator practices what it preaches
- Responsive, accessible, print-friendly
- Entrance animations with prefers-reduced-motion support
- Mock previews are CSS-only (no screenshots, no external images)
