"""
Codex Visibility Dashboard
===========================
Engineering Visibility Dashboard for Codex Pilot — Fortune 500 Retail Deployment.

Simulates and visualizes Codex usage data across teams, workflows, and risk levels.
Designed for a live sales enablement demo.

Run: streamlit run app.py
"""

import json
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OPENAI_GREEN = "#10A37F"
RISK_COLORS = {"green": "#27AE60", "yellow": "#F39C12", "red": "#E74C3C"}
WORKFLOW_COLORS = {
    "code_understanding": "#10A37F",
    "test_generation": "#9B59B6",
    "impact_analysis": "#3498DB",
    "docs_refactoring": "#E67E22",
}
BACKGROUND_DARK = "#0E1117"
CARD_BG = "#1E1E2E"

# ---------------------------------------------------------------------------
# Page config — must be the first Streamlit command
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Codex Visibility Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------

st.markdown(
    f"""
    <style>
    /* Global */
    .stApp {{
        background-color: {BACKGROUND_DARK};
    }}

    /* Metric cards */
    div[data-testid="stMetric"] {{
        background-color: {CARD_BG};
        border: 1px solid #2D2D3D;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }}
    div[data-testid="stMetric"] label {{
        color: #8E8EA0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.03em;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: #FFFFFF !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}

    /* Header styling */
    .dashboard-header {{
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }}
    .dashboard-header h1 {{
        color: #FFFFFF;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }}
    .dashboard-header .accent {{
        color: {OPENAI_GREEN};
    }}
    .dashboard-header p {{
        color: #8E8EA0;
        font-size: 1.05rem;
        margin-top: 0;
    }}

    /* Section headers */
    .section-header {{
        color: #FFFFFF;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid {OPENAI_GREEN};
        display: inline-block;
    }}

    /* Chat section */
    .chat-container {{
        background-color: {CARD_BG};
        border: 1px solid #2D2D3D;
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 0.5rem;
    }}
    .chat-response {{
        background-color: #262637;
        border-left: 3px solid {OPENAI_GREEN};
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-top: 12px;
        color: #E0E0E0;
        font-size: 0.95rem;
        line-height: 1.6;
    }}
    .chat-hint {{
        color: #6E6E80;
        font-size: 0.82rem;
        margin-top: 8px;
        font-style: italic;
    }}

    /* Footer */
    .dashboard-footer {{
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #6E6E80;
        font-size: 0.9rem;
        border-top: 1px solid #2D2D3D;
        margin-top: 2rem;
    }}
    .dashboard-footer .accent {{
        color: {OPENAI_GREEN};
        font-weight: 600;
    }}

    /* Risk badge */
    .risk-badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #FFFFFF;
    }}
    .risk-green  {{ background-color: {RISK_COLORS["green"]}; }}
    .risk-yellow {{ background-color: {RISK_COLORS["yellow"]}; }}
    .risk-red    {{ background-color: {RISK_COLORS["red"]}; }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: #161622;
        border-right: 1px solid #2D2D3D;
    }}
    section[data-testid="stSidebar"] .stMarkdown h2 {{
        color: {OPENAI_GREEN} !important;
        font-size: 1.1rem !important;
    }}

    /* Plotly chart containers */
    .stPlotlyChart {{
        border-radius: 12px;
        overflow: hidden;
    }}

    /* Dataframe styling */
    .stDataFrame {{
        border-radius: 8px;
        overflow: hidden;
    }}

    /* Divider */
    hr {{
        border-color: #2D2D3D !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load Codex usage data from the JSON file."""
    data_path = Path(__file__).parent / "data" / "codex_usage.json"

    if not data_path.exists():
        st.error(
            f"**Data file not found** at `{data_path}`.\n\n"
            "To generate the simulated data, create a JSON file at "
            "`dashboard/data/codex_usage.json` with the expected schema.\n\n"
            "Expected structure:\n"
            "```json\n"
            '{\n  "metadata": {...},\n  "queries": [\n'
            '    {"id": "Q-0001", "timestamp": "...", "team": "...", ...}\n'
            "  ]\n}\n```"
        )
        st.stop()

    with open(data_path, "r") as f:
        raw = json.load(f)

    df = pd.DataFrame(raw["queries"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    return df


df_raw = load_data()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown(
        f'<h2 style="color:{OPENAI_GREEN}; margin-bottom:0.2rem;">Filters</h2>',
        unsafe_allow_html=True,
    )
    st.caption("All charts update in real time.")

    st.markdown("---")

    # Team filter
    all_teams = sorted(df_raw["team"].unique())
    selected_teams = st.multiselect(
        "Team",
        options=all_teams,
        default=all_teams,
        help="Filter by engineering team",
    )

    # Date range filter
    min_date = df_raw["date"].min()
    max_date = df_raw["date"].max()
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter by query date",
    )

    # Workflow filter
    all_workflows = sorted(df_raw["workflow"].unique())
    workflow_labels = {w: w.replace("_", " ").title() for w in all_workflows}
    selected_workflows = st.multiselect(
        "Workflow",
        options=all_workflows,
        default=all_workflows,
        format_func=lambda w: workflow_labels.get(w, w),
        help="Filter by Codex workflow type",
    )

    # Risk level filter
    all_risks = ["green", "yellow", "red"]
    available_risks = [r for r in all_risks if r in df_raw["risk_level"].unique()]
    selected_risks = st.multiselect(
        "Risk level",
        options=available_risks,
        default=available_risks,
        help="Filter by risk classification",
    )

    st.markdown("---")
    st.markdown(
        f'<p style="color:#6E6E80; font-size:0.78rem; text-align:center;">'
        f"Data: {len(df_raw)} queries across {df_raw['team'].nunique()} teams</p>",
        unsafe_allow_html=True,
    )

# Apply filters
# Handle single-date selection (date_input returns a single date instead of tuple)
if isinstance(date_range, tuple) and len(date_range) == 2:
    date_start, date_end = date_range
else:
    date_start = date_range if not isinstance(date_range, tuple) else date_range[0]
    date_end = date_start

df = df_raw[
    (df_raw["team"].isin(selected_teams))
    & (df_raw["date"] >= date_start)
    & (df_raw["date"] <= date_end)
    & (df_raw["workflow"].isin(selected_workflows))
    & (df_raw["risk_level"].isin(selected_risks))
].copy()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown(
    '<div class="dashboard-header">'
    '<h1>Engineering <span class="accent">Visibility</span> Dashboard</h1>'
    "<p>Codex Pilot &mdash; Week 1&ndash;2 | Platform Team + Early Adopters</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Top metrics row
# ---------------------------------------------------------------------------

if df.empty:
    st.warning("No data matches the current filters. Adjust the sidebar filters.")
    st.stop()

total_queries = len(df)
active_engineers = df["engineer"].nunique()
avg_response = df["codex_response_time_seconds"].mean()
code_understanding_pct = (
    (df["workflow"] == "code_understanding").sum() / total_queries * 100
    if total_queries > 0
    else 0
)
risk_events = df[df["risk_level"].isin(["yellow", "red"])].shape[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Queries", f"{total_queries:,}")
col2.metric("Active Engineers", f"{active_engineers}")
col3.metric("Avg Response Time", f"{avg_response:.1f}s")
col4.metric("Code Understanding", f"{code_understanding_pct:.0f}%")
col5.metric("Risk Events", f"{risk_events}", delta=None)

st.markdown("")  # spacer

# ---------------------------------------------------------------------------
# Main visualization — Interactive Bubble Chart
# ---------------------------------------------------------------------------

st.markdown(
    '<div class="section-header">Usage Map &mdash; Team x Workflow</div>',
    unsafe_allow_html=True,
)

# Aggregate data for the bubble chart
bubble_data = (
    df.groupby(["team", "workflow"])
    .agg(
        count=("id", "size"),
        green=("risk_level", lambda x: (x == "green").sum()),
        yellow=("risk_level", lambda x: (x == "yellow").sum()),
        red=("risk_level", lambda x: (x == "red").sum()),
    )
    .reset_index()
)


def dominant_risk(row: pd.Series) -> str:
    """Return the proportionally dominant risk level for a given row."""
    total = row["green"] + row["yellow"] + row["red"]
    if total == 0:
        return "green"
    if row["red"] / total > 0.10:
        return "red"
    if row["yellow"] / total > 0.30:
        return "yellow"
    return "green"


bubble_data["dominant_risk"] = bubble_data.apply(dominant_risk, axis=1)
bubble_data["risk_breakdown"] = bubble_data.apply(
    lambda r: f"Green: {r['green']}  |  Yellow: {r['yellow']}  |  Red: {r['red']}",
    axis=1,
)
bubble_data["workflow_label"] = bubble_data["workflow"].apply(
    lambda w: w.replace("_", " ").title()
)

fig_bubble = px.scatter(
    bubble_data,
    x="team",
    y="workflow_label",
    size="count",
    color="dominant_risk",
    color_discrete_map=RISK_COLORS,
    size_max=65,
    hover_data={
        "team": True,
        "workflow_label": True,
        "count": True,
        "risk_breakdown": True,
        "dominant_risk": False,
    },
    labels={
        "team": "Team",
        "workflow_label": "Workflow",
        "count": "Queries",
        "risk_breakdown": "Risk Breakdown",
    },
)

fig_bubble.update_layout(
    plot_bgcolor="#1A1A2E",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E0E0E0", size=13),
    height=460,
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        title="Dominant Risk",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(0,0,0,0)",
    ),
    xaxis=dict(
        showgrid=False,
        title="",
        categoryorder="total descending",
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#2D2D3D",
        title="",
    ),
)

fig_bubble.update_traces(
    marker=dict(
        line=dict(width=1, color="#2D2D3D"),
        opacity=0.88,
    ),
)

st.plotly_chart(fig_bubble, use_container_width=True)

# ---------------------------------------------------------------------------
# Two-column layout: Daily trend + Team adoption
# ---------------------------------------------------------------------------

col_left, col_right = st.columns([3, 2])

# --- Daily usage trend ---
with col_left:
    st.markdown(
        '<div class="section-header">Daily Usage Trend</div>',
        unsafe_allow_html=True,
    )

    daily = (
        df.groupby(["date", "workflow"])
        .size()
        .reset_index(name="count")
    )
    daily["workflow_label"] = daily["workflow"].apply(
        lambda w: w.replace("_", " ").title()
    )

    fig_daily = px.line(
        daily,
        x="date",
        y="count",
        color="workflow_label",
        color_discrete_map={
            k.replace("_", " ").title(): v for k, v in WORKFLOW_COLORS.items()
        },
        markers=True,
        labels={"date": "Date", "count": "Queries", "workflow_label": "Workflow"},
    )

    fig_daily.update_layout(
        plot_bgcolor="#1A1A2E",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E0E0E0", size=12),
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="#2D2D3D", title="Queries"),
    )

    fig_daily.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig_daily, use_container_width=True)

# --- Team adoption ---
with col_right:
    st.markdown(
        '<div class="section-header">Team Adoption</div>',
        unsafe_allow_html=True,
    )

    team_counts = (
        df.groupby("team")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=True)
    )

    fig_teams = px.bar(
        team_counts,
        x="count",
        y="team",
        orientation="h",
        labels={"count": "Queries", "team": ""},
        color_discrete_sequence=[OPENAI_GREEN],
    )

    fig_teams.update_layout(
        plot_bgcolor="#1A1A2E",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E0E0E0", size=12),
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor="#2D2D3D", title="Queries"),
        yaxis=dict(showgrid=False, title=""),
        showlegend=False,
    )

    fig_teams.update_traces(
        marker=dict(
            line=dict(width=0),
            opacity=0.9,
        ),
        text=team_counts["count"],
        textposition="outside",
        textfont=dict(color="#E0E0E0", size=12),
    )

    st.plotly_chart(fig_teams, use_container_width=True)

# ---------------------------------------------------------------------------
# Risk panel
# ---------------------------------------------------------------------------

st.markdown(
    '<div class="section-header">Risk Events</div>',
    unsafe_allow_html=True,
)

risk_df = df[df["risk_level"].isin(["yellow", "red"])].copy()

if risk_df.empty:
    st.info("No yellow or red risk events in the current filter selection.")
else:
    # Summary row
    yellow_count = (risk_df["risk_level"] == "yellow").sum()
    red_count = (risk_df["risk_level"] == "red").sum()

    rc1, rc2, rc3 = st.columns([1, 1, 4])
    rc1.metric("Yellow", yellow_count)
    rc2.metric("Red", red_count)
    with rc3:
        st.markdown("")  # spacer alignment

    # Risk events table
    risk_display = risk_df[
        [
            "timestamp",
            "team",
            "engineer",
            "target_module",
            "risk_level",
            "prompt_summary",
        ]
    ].copy()
    risk_display["timestamp"] = risk_display["timestamp"].dt.strftime(
        "%Y-%m-%d %H:%M"
    )
    risk_display.columns = [
        "Timestamp",
        "Team",
        "Engineer",
        "Target Module",
        "Risk",
        "Prompt Summary",
    ]
    risk_display = risk_display.sort_values("Timestamp", ascending=False).reset_index(
        drop=True
    )

    # Color-code the Risk column with badges
    def style_risk(val: str) -> str:
        color = RISK_COLORS.get(val, "#FFFFFF")
        return f"color: {color}; font-weight: 700;"

    # pandas >= 2.1 renamed applymap → map; fall back for older versions
    _map_fn = getattr(risk_display.style, "map", None) or risk_display.style.applymap
    styled = _map_fn(style_risk, subset=["Risk"])
    st.dataframe(
        styled,
        use_container_width=True,
        height=min(len(risk_display) * 40 + 60, 350),
    )

# ---------------------------------------------------------------------------
# Chat-to-visual section
# ---------------------------------------------------------------------------

st.markdown("")  # spacer
st.markdown(
    '<div class="section-header">Ask About the Data</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="chat-container">',
    unsafe_allow_html=True,
)

user_query = st.text_input(
    "Ask about the data...",
    placeholder="e.g., Show security queries, Which team is using Codex most?",
    label_visibility="collapsed",
    key="chat_input",
)


def _fuzzy_match(query: str, keywords: list[str]) -> bool:
    """Check if any keyword appears in the lowered query."""
    q = query.lower().strip()
    return any(k in q for k in keywords)


if user_query:
    query_lower = user_query.lower().strip()

    # --- Security ---
    if _fuzzy_match(query_lower, ["security", "danger", "threat", "yellow", "red"]):
        security_df = df[df["risk_level"].isin(["yellow", "red"])]
        total_risk = len(security_df)
        st.markdown(
            f'<div class="chat-response">'
            f"<strong>Security & Risk Overview</strong><br><br>"
            f"Found <strong>{total_risk}</strong> queries flagged yellow or red "
            f"out of {len(df)} total ({total_risk / len(df) * 100:.1f}%).<br><br>"
            f"Teams involved: {', '.join(security_df['team'].unique())}.<br>"
            f"Modules affected: {', '.join(security_df['target_module'].unique())}."
            f"</div>",
            unsafe_allow_html=True,
        )

        if not security_df.empty:
            # Filtered bubble chart for risk events
            risk_bubble = (
                security_df.groupby(["team", "workflow"])
                .agg(
                    count=("id", "size"),
                    yellow=("risk_level", lambda x: (x == "yellow").sum()),
                    red=("risk_level", lambda x: (x == "red").sum()),
                )
                .reset_index()
            )
            risk_bubble["dominant_risk"] = risk_bubble.apply(
                lambda r: "red" if r["red"] > 0 else "yellow", axis=1
            )
            risk_bubble["workflow_label"] = risk_bubble["workflow"].apply(
                lambda w: w.replace("_", " ").title()
            )

            fig_risk = px.scatter(
                risk_bubble,
                x="team",
                y="workflow_label",
                size="count",
                color="dominant_risk",
                color_discrete_map=RISK_COLORS,
                size_max=50,
                labels={
                    "team": "Team",
                    "workflow_label": "Workflow",
                    "count": "Queries",
                },
                title="Risk Events by Team and Workflow",
            )
            fig_risk.update_layout(
                plot_bgcolor="#1A1A2E",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E0E0"),
                height=350,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_risk, use_container_width=True)

    # --- Most active / Which team ---
    elif _fuzzy_match(query_lower, ["most", "which team", "top team", "adoption", "active"]):
        team_rank = (
            df.groupby("team")
            .agg(
                queries=("id", "size"),
                engineers=("engineer", "nunique"),
                avg_response=("codex_response_time_seconds", "mean"),
            )
            .sort_values("queries", ascending=False)
            .reset_index()
        )
        top = team_rank.iloc[0]
        st.markdown(
            f'<div class="chat-response">'
            f"<strong>Team Adoption Ranking</strong><br><br>"
            f"<strong>{top['team']}</strong> leads with <strong>{int(top['queries'])}</strong> queries "
            f"from <strong>{int(top['engineers'])}</strong> engineers "
            f"(avg response: {top['avg_response']:.1f}s).<br><br>"
            f"Full ranking:<br>"
            + "<br>".join(
                f"&nbsp;&nbsp;{i+1}. {r['team']} &mdash; {int(r['queries'])} queries, "
                f"{int(r['engineers'])} engineers"
                for i, r in team_rank.iterrows()
            )
            + "</div>",
            unsafe_allow_html=True,
        )

        # Highlight bar chart
        colors = [
            OPENAI_GREEN if t == top["team"] else "#3D3D5C"
            for t in team_rank["team"]
        ]
        fig_highlight = go.Figure(
            go.Bar(
                x=team_rank["queries"],
                y=team_rank["team"],
                orientation="h",
                marker_color=colors,
                text=team_rank["queries"],
                textposition="outside",
                textfont=dict(color="#E0E0E0"),
            )
        )
        fig_highlight.update_layout(
            plot_bgcolor="#1A1A2E",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E0E0E0"),
            height=300,
            margin=dict(l=10, r=40, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="#2D2D3D", title="Queries"),
            yaxis=dict(showgrid=False, title="", autorange="reversed"),
        )
        st.plotly_chart(fig_highlight, use_container_width=True)

    # --- Onboarding ---
    elif _fuzzy_match(query_lower, ["onboarding", "onboard", "ramp", "new hire", "new dev"]):
        if "impact_category" in df.columns:
            onboard_df = df[df["impact_category"] == "onboarding"]
        else:
            onboard_df = pd.DataFrame()

        if onboard_df.empty:
            st.markdown(
                '<div class="chat-response">'
                "No onboarding-categorized queries found in the current filter selection."
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            onboard_pct = len(onboard_df) / len(df) * 100
            onboard_teams = onboard_df["team"].value_counts()
            avg_session = onboard_df["session_duration_seconds"].mean()
            st.markdown(
                f'<div class="chat-response">'
                f"<strong>Onboarding Impact</strong><br><br>"
                f"<strong>{len(onboard_df)}</strong> queries ({onboard_pct:.0f}% of total) "
                f"categorized as onboarding-related.<br>"
                f"Average session: <strong>{avg_session:.0f}s</strong> "
                f"({avg_session / 60:.1f} min).<br><br>"
                f"Breakdown by team:<br>"
                + "<br>".join(
                    f"&nbsp;&nbsp;{team}: {count} queries"
                    for team, count in onboard_teams.items()
                )
                + "</div>",
                unsafe_allow_html=True,
            )

            # Onboarding trend
            onboard_daily = (
                onboard_df.groupby("date").size().reset_index(name="count")
            )
            fig_onboard = px.bar(
                onboard_daily,
                x="date",
                y="count",
                labels={"date": "Date", "count": "Onboarding Queries"},
                color_discrete_sequence=[OPENAI_GREEN],
                title="Onboarding Queries by Day",
            )
            fig_onboard.update_layout(
                plot_bgcolor="#1A1A2E",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E0E0"),
                height=280,
                margin=dict(l=10, r=10, t=50, b=10),
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(showgrid=True, gridcolor="#2D2D3D", title="Queries"),
            )
            st.plotly_chart(fig_onboard, use_container_width=True)

    # --- Payments ---
    elif _fuzzy_match(query_lower, ["payment", "pay", "checkout", "transaction", "module"]):
        payment_df = df[
            df["target_module"].str.contains("payment|pay|checkout|transaction", case=False, na=False)
        ]

        if payment_df.empty:
            st.markdown(
                '<div class="chat-response">'
                "No payment-related queries found in the current filter selection. "
                "Try broadening your date range or team filters."
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            modules = payment_df["target_module"].value_counts()
            st.markdown(
                f'<div class="chat-response">'
                f"<strong>Payment Module Activity</strong><br><br>"
                f"Found <strong>{len(payment_df)}</strong> queries targeting payment-related modules.<br><br>"
                f"Modules:<br>"
                + "<br>".join(
                    f"&nbsp;&nbsp;<code>{mod}</code> &mdash; {count} queries"
                    for mod, count in modules.items()
                )
                + f"<br><br>Teams: {', '.join(payment_df['team'].unique())}.<br>"
                f"Workflows: {', '.join(payment_df['workflow'].apply(lambda w: w.replace('_', ' ').title()).unique())}."
                f"</div>",
                unsafe_allow_html=True,
            )

            # Payment queries table
            pay_display = payment_df[
                ["timestamp", "team", "engineer", "workflow", "target_module", "prompt_summary"]
            ].copy()
            pay_display["timestamp"] = pay_display["timestamp"].dt.strftime(
                "%Y-%m-%d %H:%M"
            )
            pay_display["workflow"] = pay_display["workflow"].apply(
                lambda w: w.replace("_", " ").title()
            )
            pay_display.columns = [
                "Timestamp", "Team", "Engineer", "Workflow", "Module", "Prompt Summary"
            ]
            st.dataframe(
                pay_display.sort_values("Timestamp", ascending=False).reset_index(drop=True),
                use_container_width=True,
                height=min(len(pay_display) * 40 + 60, 300),
            )

    # --- Fallback ---
    else:
        st.markdown(
            '<div class="chat-response">'
            "Try one of these queries:<br><br>"
            "&nbsp;&nbsp;&bull;&nbsp; <strong>Show security queries</strong> &mdash; "
            "filter to yellow/red risk events<br>"
            "&nbsp;&nbsp;&bull;&nbsp; <strong>Which team is using Codex most?</strong> &mdash; "
            "team adoption ranking<br>"
            "&nbsp;&nbsp;&bull;&nbsp; <strong>Show onboarding impact</strong> &mdash; "
            "onboarding-category metrics<br>"
            "&nbsp;&nbsp;&bull;&nbsp; <strong>What are engineers working on in payments?</strong> &mdash; "
            "payment module deep dive"
            "</div>",
            unsafe_allow_html=True,
        )

else:
    st.markdown(
        '<div class="chat-hint">'
        'Try: "Show security queries", "Which team is using Codex most?", '
        '"Show onboarding impact", or "What are engineers working on in payments?"'
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown(
    '<div class="dashboard-footer">'
    'Built in 48 hours using Codex. Every query generates data. '
    '<span class="accent">Data makes engineering visible.</span>'
    "</div>",
    unsafe_allow_html=True,
)
