#!/usr/bin/env python3
"""Generate Codex Enterprise Enablement PDF Deck v2.

Pixel-perfect 16:9 PDF slides for full-screen presentation.
Each page = one slide at 13.333" x 7.5" (960pt x 540pt).
"""

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import os

# Page dimensions: 16:9
W = 13.333 * inch
H = 7.5 * inch

# Colors
DARK_BG     = HexColor('#0D0D0D')
DARK_NAVY   = HexColor('#1A1A2E')
OAI_GREEN   = HexColor('#10A37F')
ACCENT_BLUE = HexColor('#3A6B9F')
ACCENT_ORANGE = HexColor('#E76F51')
ACCENT_RED  = HexColor('#C0392B')
ACCENT_PURPLE = HexColor('#6C5CE7')
LIGHT_GRAY  = HexColor('#F5F5F5')
MED_GRAY    = HexColor('#888888')
DARK_TEXT    = HexColor('#2D2D2D')
SOFT_WHITE  = HexColor('#F8F9FA')
CALLOUT_BG  = HexColor('#E8F5F0')
VP_CALLOUT  = HexColor('#FDF2E9')
DIR_CALLOUT = HexColor('#E8EEF8')
MUTED_TEXT  = HexColor('#9999BB')
MUTED_LIGHT = HexColor('#BBBBCC')
MUTED_DARK  = HexColor('#777799')
LABEL_COLOR = HexColor('#CCCCDD')

FONT = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'
FONT_ITALIC = 'Helvetica-Oblique'
FONT_BOLD_ITALIC = 'Helvetica-BoldOblique'


def rect(c, x, y, w, h, fill=None, stroke=None, stroke_width=1, radius=0):
    """Draw a rectangle. y is from TOP of page."""
    # Convert top-down y to bottom-up
    by = H - y - h
    c.saveState()
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(stroke_width)
    else:
        c.setStrokeColor(fill if fill else white)
        c.setLineWidth(0)
    if radius > 0:
        c.roundRect(x, by, w, h, radius, fill=1 if fill else 0, stroke=1 if stroke else 0)
    else:
        c.rect(x, by, w, h, fill=1 if fill else 0, stroke=1 if stroke else 0)
    c.restoreState()


def text(c, x, y, txt, size=18, font=FONT, color=DARK_TEXT, align='left', max_width=None):
    """Draw text. y is from TOP of page."""
    by = H - y - size * 0.4  # baseline adjustment
    c.saveState()
    c.setFillColor(color)
    c.setFont(font, size)
    if align == 'center' and max_width:
        tw = c.stringWidth(txt, font, size)
        x = x + (max_width - tw) / 2
    elif align == 'right' and max_width:
        tw = c.stringWidth(txt, font, size)
        x = x + max_width - tw
    c.drawString(x, by, txt)
    c.restoreState()


def multiline(c, x, y, lines, size=16, color=DARK_TEXT, spacing=1.35, font=FONT):
    """Draw multiple lines of text. Each item is (text, font_override_or_None)."""
    cy = y
    line_h = size * spacing
    for txt, f in lines:
        if txt:
            text(c, x, cy, txt, size=size, font=f or font, color=color)
        cy += line_h


def accent_bar(c, x, y, w, h, color=OAI_GREEN):
    rect(c, x, y, w, h, fill=color)


def circle(c, x, y, r, fill=None):
    """Draw filled circle. x,y = center, from top."""
    by = H - y
    c.saveState()
    if fill:
        c.setFillColor(fill)
    c.setStrokeColor(fill if fill else white)
    c.setLineWidth(0)
    c.circle(x, by, r, fill=1, stroke=0)
    c.restoreState()


# ================================================================
# SLIDE 1: TITLE
# ================================================================
def slide_1(c):
    rect(c, 0, 0, W, H, fill=DARK_BG)
    accent_bar(c, 0, 0, W, 4)

    text(c, 1.5*inch, 1.6*inch, 'Governed Codex Adoption',
         size=48, font=FONT_BOLD, color=white)
    accent_bar(c, 1.5*inch, 2.75*inch, 3*inch, 4, color=OAI_GREEN)

    text(c, 1.5*inch, 3.1*inch,
         'Improve code understanding, quality, and onboarding without losing control',
         size=22, font=FONT, color=LABEL_COLOR)

    text(c, 1.5*inch, 4.0*inch, 'Enterprise Enablement Session',
         size=16, font=FONT_ITALIC, color=MUTED_TEXT)

    text(c, 1.5*inch, 5.2*inch, 'Prepared for:',
         size=12, font=FONT_BOLD, color=OAI_GREEN)
    text(c, 1.5*inch, 5.5*inch, 'Director of Engineering  |  VP of IT',
         size=14, font=FONT, color=MUTED_LIGHT)
    text(c, 1.5*inch, 5.9*inch, 'March 2026  |  OpenAI Enterprise',
         size=12, font=FONT, color=MUTED_DARK)


# ================================================================
# SLIDE 2: FOUR PROBLEMS. ONE ROOT CAUSE.
# ================================================================
def slide_2(c):
    rect(c, 0, 0, W, H, fill=SOFT_WHITE)
    accent_bar(c, 0, 0, W, 5, color=OAI_GREEN)

    text(c, 0.8*inch, 0.45*inch, 'Four Problems. One Root Cause.',
         size=28, font=FONT_BOLD, color=DARK_NAVY)
    accent_bar(c, 0.8*inch, 1.15*inch, 2.5*inch, 3, color=OAI_GREEN)

    # Left — What We Heard
    text(c, 0.8*inch, 1.5*inch, 'What We Heard in Discovery',
         size=20, font=FONT_BOLD, color=ACCENT_BLUE)

    left_items = [
        '\u2022  15-year-old checkout code nobody understands',
        '',
        '\u2022  Test coverage gaps \u2014 teams afraid to refactor',
        '',
        '\u2022  Prior tool rollouts stalled due to uneven',
        '    adoption and weak governance',
        '',
        '\u2022  No visibility into what developers were generating',
    ]
    cy = 2.15*inch
    for item in left_items:
        if item:
            text(c, 0.8*inch, cy, item, size=14, color=DARK_TEXT)
        cy += 0.27*inch

    # Divider
    accent_bar(c, 6.45*inch, 1.5*inch, 2, 4.5*inch, color=MED_GRAY)

    # Right — The Insight
    text(c, 6.8*inch, 1.5*inch, 'The Insight: One Root Cause',
         size=20, font=FONT_BOLD, color=ACCENT_ORANGE)

    right_items = [
        '\u2192  Invisible codebase \u2192 devs can\'t understand it',
        '',
        '\u2192  Invisible quality \u2192 teams can\'t prioritize',
        '',
        '\u2192  Invisible usage \u2192 leadership can\'t govern',
        '',
        '\u2192  Invisible impact \u2192 leadership can\'t justify scale',
    ]
    cy = 2.15*inch
    for item in right_items:
        if item:
            text(c, 6.8*inch, cy, item, size=14, color=DARK_TEXT)
        cy += 0.27*inch

    # Bottom callout
    rect(c, 0.5*inch, 6.2*inch, 12.3*inch, 0.85*inch,
         fill=CALLOUT_BG, stroke=OAI_GREEN, stroke_width=1.5, radius=8)
    text(c, 0.7*inch, 6.35*inch,
         'All four problems share one root cause: invisibility. Codex helps teams work in the',
         size=14, font=FONT_BOLD, color=DARK_NAVY, align='center', max_width=12*inch)
    text(c, 0.7*inch, 6.6*inch,
         'codebase while giving leadership evidence to govern rollout.',
         size=14, font=FONT_BOLD, color=DARK_NAVY, align='center', max_width=12*inch)


# ================================================================
# SLIDE 3: CODEX IN THE WORKFLOW
# ================================================================
def slide_3(c):
    rect(c, 0, 0, W, H, fill=SOFT_WHITE)
    accent_bar(c, 0, 0, W, 5, color=OAI_GREEN)

    text(c, 0.8*inch, 0.45*inch, 'Codex in the Workflow: Local Context, Managed Controls',
         size=28, font=FONT_BOLD, color=DARK_NAVY)
    accent_bar(c, 0.8*inch, 1.15*inch, 2.5*inch, 3, color=OAI_GREEN)

    # Left box — Developer Machine
    rect(c, 0.5*inch, 1.6*inch, 5.5*inch, 4.0*inch,
         fill=DIR_CALLOUT, stroke=ACCENT_BLUE, stroke_width=1.5, radius=8)
    text(c, 0.7*inch, 1.72*inch, 'DEVELOPER MACHINE',
         size=14, font=FONT_BOLD, color=ACCENT_BLUE, align='center', max_width=5.1*inch)

    # Code Repo sub-box
    rect(c, 0.8*inch, 2.3*inch, 4.9*inch, 0.85*inch,
         fill=white, stroke=MED_GRAY, stroke_width=1, radius=6)
    text(c, 0.95*inch, 2.4*inch, 'Code Repository',
         size=13, font=FONT_BOLD, color=DARK_TEXT)
    text(c, 0.95*inch, 2.7*inch, 'Source files, dependencies, tests, AGENTS.md',
         size=11, color=MED_GRAY)

    # Codex sub-box
    rect(c, 0.8*inch, 3.35*inch, 4.9*inch, 0.85*inch,
         fill=white, stroke=OAI_GREEN, stroke_width=1, radius=6)
    text(c, 0.95*inch, 3.45*inch, 'Codex',
         size=13, font=FONT_BOLD, color=OAI_GREEN)
    text(c, 0.95*inch, 3.75*inch, 'Read \u2192 Plan \u2192 Edit \u2192 Run \u2192 Verify',
         size=11, color=MED_GRAY)

    # Sandbox sub-box
    rect(c, 0.8*inch, 4.4*inch, 4.9*inch, 0.85*inch,
         fill=VP_CALLOUT, stroke=ACCENT_ORANGE, stroke_width=1, radius=6)
    text(c, 0.95*inch, 4.5*inch, 'Kernel-Level Sandbox',
         size=13, font=FONT_BOLD, color=ACCENT_ORANGE)
    text(c, 0.95*inch, 4.8*inch, 'Seatbelt (macOS) / Landlock + seccomp (Linux)',
         size=11, color=DARK_TEXT)

    # Arrow
    text(c, 6.05*inch, 2.9*inch, '\u2192',
         size=42, font=FONT_BOLD, color=OAI_GREEN, align='center', max_width=1.2*inch)
    text(c, 6.0*inch, 3.5*inch, 'Relevant',
         size=10, font=FONT_ITALIC, color=MED_GRAY, align='center', max_width=1.3*inch)
    text(c, 6.0*inch, 3.7*inch, 'context only',
         size=10, font=FONT_ITALIC, color=MED_GRAY, align='center', max_width=1.3*inch)

    # Right box — OpenAI Cloud
    rect(c, 7.3*inch, 1.6*inch, 5.5*inch, 4.0*inch,
         fill=CALLOUT_BG, stroke=OAI_GREEN, stroke_width=1.5, radius=8)
    text(c, 7.5*inch, 1.72*inch, 'OPENAI CLOUD',
         size=14, font=FONT_BOLD, color=OAI_GREEN, align='center', max_width=5.1*inch)

    # Models sub-box
    rect(c, 7.6*inch, 2.3*inch, 4.9*inch, 0.85*inch,
         fill=white, stroke=OAI_GREEN, stroke_width=1, radius=6)
    text(c, 7.75*inch, 2.4*inch, 'OpenAI Models',
         size=13, font=FONT_BOLD, color=OAI_GREEN)
    text(c, 7.75*inch, 2.7*inch, 'Reasoning + code generation. No training on your data.',
         size=11, color=MED_GRAY)

    # Enterprise Controls sub-box
    rect(c, 7.6*inch, 3.35*inch, 4.9*inch, 1.95*inch,
         fill=white, stroke=ACCENT_PURPLE, stroke_width=1, radius=6)
    text(c, 7.75*inch, 3.45*inch, 'Enterprise Controls',
         size=13, font=FONT_BOLD, color=ACCENT_PURPLE)
    controls = [
        '\u2022  SAML SSO + SCIM provisioning',
        '\u2022  RBAC + audit logging + usage reporting',
        '\u2022  Usage analytics dashboard',
        '\u2022  Central policy controls',
    ]
    cy = 3.85*inch
    for item in controls:
        text(c, 7.75*inch, cy, item, size=11, color=DARK_TEXT)
        cy += 0.25*inch

    # Key differentiator callout
    rect(c, 0.5*inch, 5.85*inch, 12.3*inch, 0.6*inch,
         fill=CALLOUT_BG, stroke=OAI_GREEN, stroke_width=1.5, radius=8)
    text(c, 0.7*inch, 5.95*inch,
         'Codex is governed and observable. Teams work locally, leadership gets rollout evidence.',
         size=13, font=FONT_BOLD, color=DARK_NAVY, align='center', max_width=12*inch)
    text(c, 0.7*inch, 6.18*inch,
         'Part of OpenAI\'s enterprise suite alongside ChatGPT Enterprise + API + Frontier.',
         size=13, font=FONT_BOLD, color=DARK_NAVY, align='center', max_width=12*inch)

    # VP assurance
    rect(c, 0.5*inch, 6.65*inch, 12.3*inch, 0.5*inch,
         fill=VP_CALLOUT, stroke=ACCENT_ORANGE, stroke_width=1.5, radius=8)
    text(c, 0.7*inch, 6.73*inch,
         'VP Assurance: use a managed environment, central guardrails, and phased permissions so adoption can scale safely.',
         size=12, font=FONT_BOLD, color=DARK_TEXT, align='center', max_width=12*inch)


# ================================================================
# SLIDE 4: THE HARNESS
# ================================================================
def slide_4(c):
    rect(c, 0, 0, W, H, fill=SOFT_WHITE)
    accent_bar(c, 0, 0, W, 5, color=ACCENT_PURPLE)

    text(c, 0.8*inch, 0.45*inch, 'Your Standards Become the AI\u2019s Operating Rules',
         size=28, font=FONT_BOLD, color=DARK_NAVY)
    accent_bar(c, 0.8*inch, 1.15*inch, 2.5*inch, 3, color=ACCENT_PURPLE)

    columns = [
        ('AGENTS.md', 'Per-repo config, version-controlled', 'Team-owned',
         ['\u2022  Define what Codex can/cannot do',
          '    per repo',
          '\u2022  Cascading: org \u2192 repo \u2192 folder',
          '\u2022  Version-controlled alongside code',
          '\u2022  Engineering teams own policies',
          '',
          'Example:',
          '  "Do not modify files in /payments"',
          '  "Always run tests before committing"'],
         OAI_GREEN),

        ('Org Policy Layer', 'Central guardrails', 'IT-owned',
         ['\u2022  Set by IT/Security, enforced centrally',
          '\u2022  Overrides local AGENTS.md',
          '    when stricter',
          '\u2022  Define allowed/blocked ops globally',
          '\u2022  Versioned and reviewable',
          '',
          'Example:',
          '  "Block all direct database writes"',
          '  "Require review for security paths"'],
         ACCENT_PURPLE),

        ('Approval Modes', 'Graduated trust for operations', 'Phased rollout',
         ['\u2022  on-request \u2014 asks every time',
          '\u2022  untrusted \u2014 auto-approves safe ops',
          '\u2022  team-by-team \u2014 earned autonomy',
          '',
          'Phase mapping:',
          '  Pilot: on-request',
          '  Expand: untrusted',
          '  Scale: team-by-team decision',
          '',
          'Trust is earned, not assumed.'],
         ACCENT_BLUE),
    ]

    for i, (title, subtitle, owner, items, color) in enumerate(columns):
        x = 0.5*inch + i * 4.2*inch
        rect(c, x, 1.5*inch, 3.9*inch, 4.8*inch,
             fill=white, stroke=color, stroke_width=1.5, radius=8)
        text(c, x + 0.15*inch, 1.62*inch, title,
             size=17, font=FONT_BOLD, color=color)
        text(c, x + 0.15*inch, 2.0*inch, subtitle,
             size=12, font=FONT_ITALIC, color=MED_GRAY)
        text(c, x + 0.15*inch, 2.3*inch, owner,
             size=11, font=FONT_BOLD, color=color)
        accent_bar(c, x + 0.15*inch, 2.52*inch, 2.0*inch, 2, color=color)

        cy = 2.7*inch
        for item in items:
            if item:
                text(c, x + 0.15*inch, cy, item, size=11, color=DARK_TEXT)
            cy += 0.26*inch

    # Bottom callout
    rect(c, 0.5*inch, 6.5*inch, 12.3*inch, 0.6*inch,
         fill=CALLOUT_BG, stroke=OAI_GREEN, stroke_width=1.5, radius=8)
    text(c, 0.7*inch, 6.6*inch,
         'The harness makes rollout governable: local team instructions, central guardrails, and phased permissions.',
         size=13, font=FONT_BOLD, color=DARK_NAVY, align='center', max_width=12*inch)


# ================================================================
# SLIDE 5: THREE WORKFLOWS, PHASED ROLLOUT
# ================================================================
def slide_5(c):
    rect(c, 0, 0, W, H, fill=SOFT_WHITE)
    accent_bar(c, 0, 0, W, 5, color=OAI_GREEN)

    text(c, 0.8*inch, 0.45*inch, 'Start Read-Only. Scale on Evidence.',
         size=28, font=FONT_BOLD, color=DARK_NAVY)
    accent_bar(c, 0.8*inch, 1.15*inch, 2.5*inch, 3, color=OAI_GREEN)

    workflows = [
        ('1. Code Understanding', 'HIGHLIGHTED \u2014 Start here',
         ['\u2022  "Explain this function and its deps"',
          '\u2022  "What would break if I changed this?"',
          '\u2022  Impact analysis + dependency mapping',
          '',
          'Why first:',
          '  \u2713  Read-only = zero generation risk',
          '  \u2713  Addresses pain #1 (legacy code)',
          '  \u2713  Fastest "aha moment"',
          '  \u2713  Gateway to other workflows',
          '',
          'Why it wins:',
          '  \u2713  Immediate value for onboarding'],
         OAI_GREEN, CALLOUT_BG, True),

        ('2. Test Generation', 'Measurable coverage lift',
         ['\u2022  "Generate unit tests for this function"',
          '\u2022  "Add edge cases for payment flow"',
          '\u2022  Coverage reports before/after',
          '',
          'Why second:',
          '  \u2713  Measurable output (coverage %)',
          '  \u2713  Builds on code understanding',
          '  \u2713  Addresses test gap pain point',
          '  \u2713  Generated tests require review'],
         ACCENT_BLUE, white, False),

        ('3. Docs & Refactoring', 'Velocity improvement',
         ['\u2022  "Document this module\'s public API"',
          '\u2022  "Refactor to extract shared logic"',
          '\u2022  Inline documentation generation',
          '',
          'Why third:',
          '  \u2713  Highest autonomy, highest review',
          '  \u2713  Devs have trust by this point',
          '  \u2713  Direct velocity impact',
          '  \u2713  Requires mature harness config'],
         ACCENT_PURPLE, white, False),
    ]

    for i, (title, subtitle, items, color, bg, highlight) in enumerate(workflows):
        x = 0.5*inch + i * 4.2*inch
        rect(c, x, 1.5*inch, 3.9*inch, 4.1*inch,
             fill=bg, stroke=color, stroke_width=1.5, radius=8)
        text(c, x + 0.15*inch, 1.62*inch, title,
             size=15, font=FONT_BOLD, color=color)
        text(c, x + 0.15*inch, 1.95*inch, subtitle,
             size=11, font=FONT_BOLD_ITALIC,
             color=OAI_GREEN if highlight else MED_GRAY)
        accent_bar(c, x + 0.15*inch, 2.2*inch, 2.0*inch, 2, color=color)

        cy = 2.38*inch
        for item in items:
            if item:
                text(c, x + 0.15*inch, cy, item, size=10.5, color=DARK_TEXT)
            cy += 0.24*inch

    # Phase timeline
    accent_bar(c, 0.5*inch, 5.8*inch, 12.3*inch, 2, color=MED_GRAY)

    phases = [
        (0.5, 'WEEKS 1\u20132: Pilot',
         ['20\u201330 devs  |  Code Understanding',
          'on-request  |  weekly office hours'], OAI_GREEN),
        (4.7, 'WEEKS 3\u20136: Expand',
         ['3 teams  |  + Test Generation',
          'untrusted mode'], ACCENT_BLUE),
        (8.9, 'WEEKS 7\u201312: Scale',
         ['All engineering  |  + Docs & Refactoring',
          'team-by-team approval'], ACCENT_PURPLE),
    ]
    for px, label, desc_lines, color in phases:
        text(c, px*inch, 5.92*inch, label, size=13, font=FONT_BOLD, color=color)
        cy = 6.18*inch
        for dl in desc_lines:
            text(c, px*inch, cy, dl, size=10, color=DARK_TEXT)
            cy += 0.2*inch

    # Limitations callout
    rect(c, 0.5*inch, 6.55*inch, 7.5*inch, 0.55*inch,
         fill=VP_CALLOUT, stroke=ACCENT_ORANGE, stroke_width=1.5, radius=6)
    text(c, 0.65*inch, 6.65*inch,
         'Codex has real limitations. We show you how to work WITH them, not around them.',
         size=11.5, font=FONT_BOLD, color=DARK_TEXT)

    # Review expectation
    rect(c, 8.2*inch, 6.55*inch, 4.6*inch, 0.55*inch,
         fill=white, stroke=ACCENT_RED, stroke_width=1.5, radius=6)
    text(c, 8.35*inch, 6.65*inch,
         'All generated code = standard code review. No exceptions.',
         size=11.5, font=FONT_BOLD, color=ACCENT_RED)


# ================================================================
# SLIDE 6: THE VISIBILITY LAYER
# ================================================================
def slide_6(c):
    rect(c, 0, 0, W, H, fill=SOFT_WHITE)
    accent_bar(c, 0, 0, W, 5, color=OAI_GREEN)

    text(c, 0.8*inch, 0.45*inch, 'Same Data. Two Audiences.',
         size=28, font=FONT_BOLD, color=DARK_NAVY)
    accent_bar(c, 0.8*inch, 1.15*inch, 2.5*inch, 3, color=OAI_GREEN)

    # Dashboard mockup panel
    rect(c, 0.5*inch, 1.5*inch, 7.5*inch, 4.2*inch,
         fill=white, stroke=MED_GRAY, stroke_width=1, radius=8)
    text(c, 0.7*inch, 1.58*inch, 'VISIBILITY DASHBOARD',
         size=11, font=FONT_BOLD, color=MED_GRAY, align='center', max_width=7.1*inch)

    # Axis labels
    text(c, 0.65*inch, 5.25*inch, 'Teams \u2192',
         size=10, font=FONT_ITALIC, color=MED_GRAY)

    # Row labels
    text(c, 0.75*inch, 2.35*inch, 'Understanding', size=9, color=MED_GRAY)
    text(c, 0.75*inch, 3.35*inch, 'Test Gen', size=9, color=MED_GRAY)
    text(c, 0.75*inch, 4.35*inch, 'Docs/Refactor', size=9, color=MED_GRAY)

    # Column labels
    cols = [('Platform', 2.5, ACCENT_BLUE), ('Checkout', 3.8, ACCENT_PURPLE),
            ('Inventory', 5.1, ACCENT_ORANGE), ('Payments', 6.4, OAI_GREEN)]
    for name, x, color in cols:
        text(c, x*inch, 2.0*inch, name, size=9, font=FONT_BOLD, color=color)

    # Bubbles — Understanding row
    bubbles_u = [(2.7, 2.6, 0.38, OAI_GREEN), (3.95, 2.7, 0.28, OAI_GREEN),
                 (5.15, 2.75, 0.22, OAI_GREEN), (6.55, 2.65, 0.33, OAI_GREEN)]
    for bx, by, br, bc in bubbles_u:
        circle(c, bx*inch, by*inch, br*inch, fill=bc)

    # Bubbles — Test Gen row
    bubbles_t = [(2.75, 3.55, 0.24, OAI_GREEN), (3.98, 3.5, 0.26, ACCENT_ORANGE),
                 (5.25, 3.6, 0.15, ACCENT_ORANGE), (6.6, 3.55, 0.22, OAI_GREEN)]
    for bx, by, br, bc in bubbles_t:
        circle(c, bx*inch, by*inch, br*inch, fill=bc)

    # Bubbles — Docs row
    bubbles_d = [(2.75, 4.5, 0.17, ACCENT_ORANGE), (4.0, 4.55, 0.13, ACCENT_RED),
                 (5.25, 4.6, 0.11, ACCENT_ORANGE), (6.6, 4.5, 0.19, ACCENT_ORANGE)]
    for bx, by, br, bc in bubbles_d:
        circle(c, bx*inch, by*inch, br*inch, fill=bc)

    # Legend
    text(c, 1.0*inch, 4.95*inch,
         'Bubble size = query volume     Color = risk level (green = safe, orange = review, red = flagged)',
         size=9, font=FONT_ITALIC, color=MED_GRAY)
    text(c, 2.7*inch, 5.25*inch, 'Team \u00d7 Workflow \u00d7 Risk',
         size=12, font=FONT_BOLD, color=DARK_NAVY, align='center', max_width=3.5*inch)

    # VP View box
    rect(c, 8.3*inch, 1.5*inch, 4.5*inch, 1.95*inch,
         fill=VP_CALLOUT, stroke=ACCENT_ORANGE, stroke_width=1.5, radius=8)
    text(c, 8.45*inch, 1.62*inch, 'VP View',
         size=16, font=FONT_BOLD, color=ACCENT_ORANGE)
    accent_bar(c, 8.45*inch, 1.9*inch, 1.5*inch, 2, color=ACCENT_ORANGE)
    vp_items = ['\u2022  Usage patterns across teams', '\u2022  Risk indicators by workflow',
                '\u2022  Compliance trails, audit-ready', '\u2022  Export for security review']
    cy = 2.05*inch
    for item in vp_items:
        text(c, 8.45*inch, cy, item, size=12, color=DARK_TEXT)
        cy += 0.27*inch

    # Director View box
    rect(c, 8.3*inch, 3.65*inch, 4.5*inch, 1.95*inch,
         fill=DIR_CALLOUT, stroke=ACCENT_BLUE, stroke_width=1.5, radius=8)
    text(c, 8.45*inch, 3.77*inch, 'Director View',
         size=16, font=FONT_BOLD, color=ACCENT_BLUE)
    accent_bar(c, 8.45*inch, 4.05*inch, 1.5*inch, 2, color=ACCENT_BLUE)
    dir_items = ['\u2022  Adoption rates by team', '\u2022  Bottlenecks and friction points',
                 '\u2022  Impact metrics (coverage, velocity)', '\u2022  Team performance trends']
    cy = 4.2*inch
    for item in dir_items:
        text(c, 8.45*inch, cy, item, size=12, color=DARK_TEXT)
        cy += 0.27*inch

    # Bottom callout
    rect(c, 0.5*inch, 5.8*inch, 12.3*inch, 0.6*inch,
         fill=CALLOUT_BG, stroke=OAI_GREEN, stroke_width=1.5, radius=8)
    text(c, 0.7*inch, 5.9*inch,
         'Same data, different views. Shared language for what\'s happening and whether it\'s working.',
         size=14, font=FONT_BOLD, color=DARK_NAVY, align='center', max_width=12*inch)

    # Bottom accent
    accent_bar(c, 0.5*inch, 6.6*inch, 12.3*inch, 2, color=OAI_GREEN)
    text(c, 0.5*inch, 6.75*inch,
         'Example pilot view: adoption, risk, and workflow mix in one place.',
         size=14, font=FONT_BOLD_ITALIC, color=OAI_GREEN, align='center', max_width=12.3*inch)


# ================================================================
# SLIDE 7: NEXT STEPS
# ================================================================
def slide_7(c):
    rect(c, 0, 0, W, H, fill=DARK_BG)
    accent_bar(c, 0, 0, W, 4, color=OAI_GREEN)

    text(c, 1.5*inch, 0.85*inch, 'Next Step: Pilot in Two Weeks',
         size=36, font=FONT_BOLD, color=white)
    accent_bar(c, 1.5*inch, 1.6*inch, 2.5*inch, 4, color=OAI_GREEN)

    steps = [
        ('1', 'Select Pilot Team',
         'Platform engineering \u2014 most legacy burden, most to gain. '
         'Their success becomes the proof point for expansion. '
         '20\u201330 developers. Code Understanding only.',
         OAI_GREEN),
        ('2', 'IT/Security Workshop \u2014 Day 1, Not Day 30',
         'Joint session with your security team and OpenAI to configure '
         'policy controls, SSO integration, data classification, and audit expectations. '
         'Security is a partner, not a gate.',
         ACCENT_BLUE),
        ('3', 'Define Pass/Fail Metrics Before the Pilot Starts',
         'Agree on measurable success criteria in writing before anyone '
         'touches the tool. If we hit the metric, evidence drives expansion. '
         'If we don\'t, you have a fair, data-driven decision.',
         ACCENT_PURPLE),
    ]

    for i, (num, title, desc, color) in enumerate(steps):
        y = 2.2*inch + i * 1.55*inch

        # Number circle
        circle(c, 1.8*inch, y + 0.22*inch, 0.25*inch, fill=color)
        text(c, 1.55*inch, y + 0.08*inch, num,
             size=22, font=FONT_BOLD, color=white, align='center', max_width=0.5*inch)

        text(c, 2.3*inch, y, title,
             size=20, font=FONT_BOLD, color=white)
        # Wrap description text manually
        words = desc.split()
        lines = []
        current = ''
        for w in words:
            test = current + (' ' if current else '') + w
            if len(test) > 95:
                lines.append(current)
                current = w
            else:
                current = test
        if current:
            lines.append(current)

        cy = y + 0.4*inch
        for line in lines:
            text(c, 2.3*inch, cy, line, size=13, color=MUTED_LIGHT)
            cy += 0.23*inch

    # Closing thesis
    accent_bar(c, 1.5*inch, 6.25*inch, 10*inch, 2, color=OAI_GREEN)
    text(c, 1.5*inch, 6.45*inch,
         '"Start visible. Stay visible. Scale on evidence."',
         size=16, font=FONT_BOLD_ITALIC, color=OAI_GREEN,
         align='center', max_width=10*inch)


# ================================================================
# BUILD PDF
# ================================================================
output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, 'codex_enablement_v2.pdf')

c = canvas.Canvas(output_path, pagesize=(W, H))
c.setTitle('Governed Codex Adoption - Enterprise Enablement')
c.setAuthor('OpenAI Enterprise')

slides = [slide_1, slide_2, slide_3, slide_4, slide_5, slide_6, slide_7]
for i, slide_fn in enumerate(slides):
    slide_fn(c)
    if i < len(slides) - 1:
        c.showPage()

c.save()
print(f'PDF saved to: {output_path}')
print(f'Pages: {len(slides)}')
print(f'Dimensions: {W/inch:.3f}" x {H/inch:.3f}" (16:9)')
