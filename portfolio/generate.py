#!/usr/bin/env python3
"""
Learning Architecture Portfolio Generator

Takes a topic YAML config and produces a self-contained HTML portfolio page.
Part of the Palette Enablement System.

Usage:
    python3 generate.py topics/taxonomy-design.yaml
    python3 generate.py topics/taxonomy-design.yaml --output dist/custom-name.html
"""

import sys
import os
import yaml
import html as html_mod
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DIST_DIR = SCRIPT_DIR / "dist"


def esc(text):
    """HTML-escape text."""
    return html_mod.escape(str(text))


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


# ── Mock preview templates ──

MOCK_OKA = """
<div class="mock-oka">
  <div class="mock-oka-top">
    <div class="mock-oka-avatar"><div class="mock-oka-eyes"><div class="mock-oka-eye"></div><div class="mock-oka-eye"></div></div><div class="mock-oka-nose"></div></div>
    <div><div class="mock-oka-name">Oka</div><div class="mock-oka-sub">Adaptive learning companion</div></div>
  </div>
  <div class="mock-oka-main">
    <div class="mock-oka-card">
      <div class="mock-oka-label">Oka says</div>
      <div class="mock-oka-response">{response}</div>
    </div>
    <div class="mock-oka-card mock-oka-focus">
      <div class="mock-oka-band">{band}</div>
      <div class="mock-oka-word">{word}</div>
      <div class="mock-oka-hint">{hint}</div>
    </div>
  </div>
  <div class="mock-oka-mic"><div class="mock-oka-mic-btn">Talk</div></div>
</div>
"""

MOCK_DASHBOARD = """
<div class="mock-dashboard">
  <div class="mock-dash-header">
    <div class="mock-dash-title"><span>{accent_word}</span> {title_rest}</div>
    <div class="mock-live"><div class="mock-live-dot"></div> Live</div>
  </div>
  <div class="mock-metrics">{metrics_html}</div>
  <div class="mock-charts">
    <div class="mock-chart">
      <div class="mock-chart-title">{chart1_title}</div>
      <div class="mock-bars">{bars_html}</div>
    </div>
    <div class="mock-chart">
      <div class="mock-chart-title">{chart2_title}</div>
      <div class="mock-bubbles">{bubbles_html}</div>
    </div>
  </div>
</div>
"""

MOCK_OBSIDIAN = """
<div class="mock-obsidian">
  <div class="mock-obs-modebar">{modes_html}</div>
  <div class="mock-obs-health">{pills_html}</div>
  <div class="mock-obs-cards">{cards_html}</div>
</div>
"""

MOCK_ENABLEMENT = """
<div class="mock-enablement">
  <div class="mock-en-title">{title}</div>
  <div class="mock-en-layers">{layers_html}</div>
</div>
"""


def render_mock_metric(label, value, color_class=""):
    cls = f' {color_class}' if color_class else ''
    return f'<div class="mock-metric"><div class="mock-metric-label">{esc(label)}</div><div class="mock-metric-value{cls}">{esc(value)}</div></div>'


def render_mock_bar(width, color, label=""):
    label_html = f'<span style="font-size:0.55rem;color:#6E6E80;white-space:nowrap;">{esc(label)}</span>' if label else ''
    return f'<div style="display:flex;align-items:center;gap:8px;"><div class="mock-bar" style="width:{width}%;background:{color};flex:1;"></div>{label_html}</div>'


def render_mock_bubble(size, color):
    return f'<div class="mock-bubble" style="width:{size}px;height:{size}px;background:{color};"></div>'


def render_obs_card(title, meta, confidence, state=""):
    cls = f' {state}' if state else ''
    color = '#27ae60' if state == 'decided' else '#f08b58' if state == 'exploring' else 'var(--accent)'
    return f'''<div class="mock-obs-card{cls}">
      <div class="mock-obs-card-title">{esc(title)}</div>
      <div class="mock-obs-card-meta">{esc(meta)}</div>
      <div class="mock-obs-confidence"><div class="mock-obs-conf-fill" style="width:{confidence}%;background:{color};"></div></div>
    </div>'''


def render_en_layer(num, cls, name, desc, chips):
    chips_html = ''.join(f'<span class="mock-en-chip">{esc(c)}</span>' for c in chips)
    return f'''<div class="mock-en-layer">
      <div class="mock-en-layer-num {cls}">{num}</div>
      <div class="mock-en-layer-content">
        <div class="mock-en-layer-name">{esc(name)}</div>
        <div class="mock-en-layer-desc">{esc(desc)}</div>
        <div class="mock-en-layer-items">{chips_html}</div>
      </div>
    </div>'''


def build_mock(project):
    """Build mock preview HTML from project config."""
    mock_type = project.get("mock", "enablement")
    mock_data = project.get("mock_data", {})

    if mock_type == "custom":
        return project.get("mock_html", '<div style="padding:40px;text-align:center;color:#888;">Custom mock</div>')

    if mock_type == "oka":
        return MOCK_OKA.format(
            response=esc(mock_data.get("response", "Let's try something fun!")),
            band=esc(mock_data.get("band", "Band: CVC")),
            word=esc(mock_data.get("word", "cat")),
            hint=esc(mock_data.get("hint", "try first → one hint → second try → simplify")),
        )

    if mock_type == "dashboard":
        metrics = mock_data.get("metrics", [
            {"label": "Total", "value": "1,234"},
            {"label": "Success", "value": "92%", "color": "green"},
        ])
        metrics_html = ''.join(render_mock_metric(m["label"], m["value"], m.get("color", "")) for m in metrics)
        bars = mock_data.get("bars", [
            {"width": 90, "color": "#10A37F", "label": "Alpha"},
            {"width": 70, "color": "#27AE60", "label": "Beta"},
        ])
        bars_html = ''.join(render_mock_bar(b["width"], b["color"], b.get("label", "")) for b in bars)
        bubbles = mock_data.get("bubbles", [
            {"size": 50, "color": "#10A37F"},
            {"size": 35, "color": "#3498DB"},
        ])
        bubbles_html = ''.join(render_mock_bubble(b["size"], b["color"]) for b in bubbles)
        return MOCK_DASHBOARD.format(
            accent_word=esc(mock_data.get("accent_word", "AI")),
            title_rest=esc(mock_data.get("title_rest", "Dashboard")),
            metrics_html=metrics_html,
            chart1_title=esc(mock_data.get("chart1_title", "Distribution")),
            chart2_title=esc(mock_data.get("chart2_title", "Coverage")),
            bars_html=bars_html,
            bubbles_html=bubbles_html,
        )

    if mock_type == "obsidian":
        modes = mock_data.get("modes", ["Explore", "Converge", "Commit"])
        active = mock_data.get("active_mode", 1)
        modes_html = ''.join(
            f'<div class="mock-obs-mode{" active" if i == active else ""}">{esc(m)}</div>'
            for i, m in enumerate(modes)
        )
        pills = mock_data.get("pills", [
            {"text": "3 Decided", "color": "green"},
            {"text": "2 Converging", "color": "yellow"},
        ])
        pills_html = ''.join(f'<div class="mock-obs-pill {p["color"]}">{esc(p["text"])}</div>' for p in pills)
        cards = mock_data.get("cards", [
            {"title": "Decision A", "meta": "Decided", "confidence": 95, "state": "decided"},
        ])
        cards_html = ''.join(render_obs_card(c["title"], c["meta"], c["confidence"], c.get("state", "")) for c in cards)
        return MOCK_OBSIDIAN.format(modes_html=modes_html, pills_html=pills_html, cards_html=cards_html)

    # Default: enablement
    layers = mock_data.get("layers", [
        {"num": 1, "cls": "l1", "name": "Layer 1", "desc": "Description", "chips": ["item"]},
    ])
    layers_html = ""
    for i, layer in enumerate(layers):
        if i > 0:
            arrow_text = mock_data.get("arrows", ["↓"])[min(i - 1, len(mock_data.get("arrows", ["↓"])) - 1)]
            layers_html += f'<div class="mock-en-arrow">{esc(arrow_text)}</div>'
        layers_html += render_en_layer(
            layer["num"], layer.get("cls", f"l{layer['num']}"),
            layer["name"], layer["desc"], layer.get("chips", [])
        )
    return MOCK_ENABLEMENT.format(
        title=esc(mock_data.get("title", "Architecture")),
        layers_html=layers_html,
    )


def render_project(project):
    """Render a full project card."""
    tags = project.get("tags", [])
    tag_colors = ["tag", "tag--green tag", "tag--orange tag", "tag--blue tag"]
    tags_html = ''.join(
        f'<span class="{tag_colors[i % len(tag_colors)]}">{esc(t)}</span>'
        for i, t in enumerate(tags)
    )

    details_html = ""
    for detail in project.get("details", []):
        items = ''.join(f'<li>{esc(item)}</li>' for item in detail.get("items", []))
        details_html += f'<div class="detail-block"><h4>{esc(detail["heading"])}</h4><ul>{items}</ul></div>'

    mock_html = build_mock(project)

    return f'''
  <div class="project">
    <div class="project-preview"><div class="project-preview-inner">{mock_html}</div></div>
    <div class="project-body">
      <div class="project-tags">{tags_html}</div>
      <h3>{esc(project.get("title", ""))}</h3>
      <p class="project-desc">{esc(project.get("description", ""))}</p>
      <div class="project-details">{details_html}</div>
    </div>
  </div>'''


def render_philosophy(items):
    cards = ''.join(
        f'<div class="phil-item"><h4>{esc(item["title"])}</h4><p>{esc(item["desc"])}</p></div>'
        for item in items
    )
    return f'<div class="philosophy"><div class="phil-grid">{cards}</div></div>'


def render_timeline(items):
    if not items:
        return ""
    entries = ""
    for item in items:
        entries += f'''
    <div class="timeline-item">
      <div class="timeline-year">{esc(item.get("year", ""))}</div>
      <div class="timeline-content">
        <div class="timeline-title">{esc(item.get("title", ""))}</div>
        <div class="timeline-place">{esc(item.get("place", ""))}</div>
        <div class="timeline-desc">{esc(item.get("desc", ""))}</div>
      </div>
    </div>'''
    return f'<div class="timeline">{entries}</div>'


def generate(config, output_path):
    """Generate complete HTML from config."""
    topic = config.get("topic", {})
    hero = config.get("hero", {})
    projects = config.get("projects", [])
    philosophy = config.get("philosophy", [])
    timeline = config.get("timeline", [])
    contact = config.get("contact", {})
    theme = config.get("theme", {})

    accent = theme.get("accent", "#635bff")
    title = topic.get("title", "Learning Architecture")
    topic_id = topic.get("id", "portfolio")

    # Build stats
    stats_html = ""
    for stat in hero.get("stats", []):
        stats_html += f'''
    <div class="hero-stat">
      <div class="hero-stat-num">{esc(stat["num"])}</div>
      <div class="hero-stat-label">{esc(stat["label"])}</div>
    </div>'''

    # Build project sections
    projects_html = ""
    for i, proj in enumerate(projects):
        section_label = proj.get("label", "Project")
        section_title = proj.get("section_title", proj.get("title", ""))
        section_desc = proj.get("section_desc", "")
        projects_html += f'''
<section class="section" id="project-{i}">
  <div class="section-header">
    <div class="section-label">{esc(section_label)}</div>
    <div class="section-title">{esc(section_title)}</div>
    <p class="section-desc">{esc(section_desc)}</p>
  </div>
  {render_project(proj)}
</section>'''

    # Build nav links
    nav_items = ''.join(
        f'<li><a href="#project-{i}">{esc(p.get("nav_label", p.get("title", f"Project {i+1}")[:20]))}</a></li>'
        for i, p in enumerate(projects)
    )
    if philosophy:
        nav_items += '<li><a href="#philosophy">Philosophy</a></li>'

    # Timeline section
    timeline_section = ""
    if timeline:
        timeline_section = f'''
<section class="section" id="journey">
  <div class="section-header">
    <div class="section-label">Journey</div>
    <div class="section-title">{esc(timeline[0].get("section_title", "The path here"))}</div>
  </div>
  {render_timeline(timeline)}
</section>'''

    # Philosophy section
    philosophy_section = ""
    if philosophy:
        philosophy_section = f'''
<section class="section" id="philosophy">
  <div class="section-header">
    <div class="section-label">Design Philosophy</div>
    <div class="section-title">How I think about this</div>
  </div>
  {render_philosophy(philosophy)}
</section>'''

    # CTA
    cta_html = ""
    if contact:
        links = ""
        if contact.get("email"):
            links += f'<a href="mailto:{esc(contact["email"])}" class="cta-link cta-link--primary">{esc(contact["email"])}</a>'
        for link in contact.get("links", []):
            links += f'<a href="{esc(link["url"])}" class="cta-link cta-link--secondary">{esc(link["label"])}</a>'
        cta_html = f'''
<section class="cta">
  <div class="cta-box">
    <h2>{esc(contact.get("headline", "Let's talk."))}</h2>
    <p>{esc(contact.get("description", ""))}</p>
    <div class="cta-links">{links}</div>
  </div>
</section>'''

    # Load the CSS template
    css_path = SCRIPT_DIR / "templates" / "portfolio.css"
    if css_path.exists():
        css = css_path.read_text()
    else:
        css = "/* CSS template not found — using inline from Stripe portfolio */"

    # Replace accent color in CSS
    css = css.replace("#635bff", accent)
    css = css.replace("rgba(99,91,255,", f"rgba({int(accent[1:3],16)},{int(accent[3:5],16)},{int(accent[5:7],16)},")

    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{esc(hero.get('description', title))}" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(hero.get('description', ''))}" />
  <title>{esc(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
{css}
  </style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <div class="nav-name">{esc(contact.get("name", ""))}</div>
    <ul class="nav-links">{nav_items}</ul>
  </div>
</nav>

<section class="hero">
  <div class="hero-label animate-in">{esc(topic.get("label", "Learning Architecture"))}</div>
  <h1 class="animate-in delay-1">{hero.get("headline", title)}</h1>
  <p class="hero-sub animate-in delay-2">{esc(hero.get("description", ""))}</p>
  <div class="hero-stats animate-in delay-3">{stats_html}</div>
</section>

{projects_html}
{timeline_section}
{philosophy_section}
{cta_html}

<footer class="footer">
  <p>{esc(contact.get("footer", ""))}</p>
</footer>

</body>
</html>'''

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(output_path)
    out.write_text(page)
    print(f"Generated: {out} ({len(page):,} bytes)")
    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate.py topics/<topic>.yaml [--output dist/<name>.html]")
        sys.exit(1)

    config_path = sys.argv[1]
    output = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output = sys.argv[idx + 1]

    config = load_config(config_path)
    topic_id = config.get("topic", {}).get("id", "portfolio")

    if not output:
        output = str(DIST_DIR / f"{topic_id}.html")

    generate(config, output)


if __name__ == "__main__":
    main()
