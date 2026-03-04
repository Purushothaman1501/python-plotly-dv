"""
=============================================================================
Student Engagement & Performance Analytics Dashboard
=============================================================================
Dataset : xAPI-Edu-Data.csv
Framework: Plotly Dash + Pandas + Plotly Express
Run      : python app.py  →  http://127.0.0.1:8050
=============================================================================
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, dash_table, Input, Output, callback

# ─────────────────────────────────────────────────────────────────────────────
# 0.  APP INITIALISATION
# ─────────────────────────────────────────────────────────────────────────────
app = Dash(__name__, title="Student Analytics Dashboard")
server = app.server  # expose Flask server for potential deployment

# ─────────────────────────────────────────────────────────────────────────────
# 1.  DATA LOADING & PRE-PROCESSING
# ─────────────────────────────────────────────────────────────────────────────
CSV_PATH = os.path.join(os.path.dirname(__file__), "xAPI-Edu-Data.csv")

REQUIRED_COLUMNS = [
    "gender", "NationalITy", "PlaceofBirth", "StageID", "GradeID",
    "SectionID", "Topic", "Semester", "raisedhands", "VisITedResources",
    "AnnouncementsView", "Discussion", "ParentAnsweringSurvey",
    "ParentschoolSatisfaction", "StudentAbsenceDays", "Class",
]

CLASS_MAP = {"L": "Low", "M": "Medium", "H": "High"}
PERF_ORDER = ["Low", "Medium", "High"]
# Palette from reference image: red=low, teal-blue=medium, lime-green=high
PERF_COLORS = {"High": "#8DC63F", "Medium": "#29ABE2", "Low": "#E05C5C"}
COLOR_SEQ = [PERF_COLORS[k] for k in PERF_ORDER]


def load_data(path: str) -> pd.DataFrame:
    """Load and validate the student dataset."""
    df = pd.read_csv(path)

    # Validate required columns
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    # Drop rows missing critical fields
    df.dropna(subset=["Class", "gender", "StageID"], inplace=True)

    # Map performance labels
    df["Class"] = df["Class"].map(CLASS_MAP).fillna(df["Class"])
    df["Class"] = pd.Categorical(df["Class"], categories=PERF_ORDER, ordered=True)

    # Friendly semester labels
    df["Semester"] = df["Semester"].replace({"F": "First", "S": "Second"})

    # Ensure numeric engagement columns
    for col in ["raisedhands", "VisITedResources", "AnnouncementsView", "Discussion"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


df_global = load_data(CSV_PATH)


def unique_opts(series: pd.Series) -> list[dict]:
    """Return sorted dropdown option dicts for a column."""
    return [{"label": v, "value": v} for v in sorted(series.dropna().unique())]


# ─────────────────────────────────────────────────────────────────────────────
# 2.  DESIGN TOKENS & INLINE STYLES
# ─────────────────────────────────────────────────────────────────────────────
FONT      = "'Inter', 'Segoe UI', sans-serif"
# ── Palette derived from reference dashboard image ──────────────────────────
BG_APP    = "#F0F4F8"          # light blue-gray page background
BG_PANEL  = "#FFFFFF"          # white card/panel background
BG_CARD   = "#EBF5FB"          # very light blue KPI card
BG_FILTER = "#FFFFFF"          # white sidebar
ACCENT    = "#29ABE2"          # teal-blue (primary brand colour)
ACCENT2   = "#8DC63F"          # lime-green (secondary brand colour)
BORDER    = "#D6E4ED"          # light blue-gray divider
TEXT_P    = "#2D3748"          # dark slate primary text
TEXT_S    = "#718096"          # medium gray secondary text
TEXT_H    = "#1A202C"          # near-black header text

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT, color=TEXT_P, size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor=BORDER,
        borderwidth=1,
        font=dict(color=TEXT_P),
    ),
    xaxis=dict(
        gridcolor="#E8EEF3",
        linecolor=BORDER,
        tickfont=dict(color=TEXT_S),
        title_font=dict(color=TEXT_S),
    ),
    yaxis=dict(
        gridcolor="#E8EEF3",
        linecolor=BORDER,
        tickfont=dict(color=TEXT_S),
        title_font=dict(color=TEXT_S),
    ),
)

style_page = {
    "fontFamily": FONT,
    "backgroundColor": BG_APP,
    "minHeight": "100vh",
    "color": TEXT_P,
    "fontSize": "13px",
}
style_header = {
    "background": f"linear-gradient(135deg, #29ABE2 0%, #1A7DAF 60%, #155E8A 100%)",
    "borderBottom": f"3px solid {ACCENT2}",
    "padding": "18px 32px",
    "display": "flex",
    "alignItems": "center",
    "gap": "16px",
    "boxShadow": "0 2px 12px rgba(41,171,226,0.25)",
}
style_body = {
    "display": "flex",
    "gap": "0",
}
style_sidebar = {
    "width": "240px",
    "minWidth": "240px",
    "backgroundColor": BG_FILTER,
    "borderRight": f"1px solid {BORDER}",
    "padding": "20px 16px",
    "minHeight": "calc(100vh - 80px)",
    "boxShadow": "2px 0 8px rgba(41,171,226,0.08)",
}
style_main = {
    "flex": "1",
    "padding": "20px 24px",
    "overflowX": "hidden",
}
style_section_title = {
    "fontSize": "12px",
    "fontWeight": "700",
    "textTransform": "uppercase",
    "letterSpacing": "1.5px",
    "color": ACCENT,
    "marginBottom": "12px",
    "marginTop": "24px",
    "borderBottom": f"2px solid {ACCENT}",
    "paddingBottom": "8px",
    "display": "flex",
    "alignItems": "center",
    "gap": "8px",
}
style_label = {
    "fontSize": "10px",
    "fontWeight": "700",
    "textTransform": "uppercase",
    "letterSpacing": "1px",
    "color": TEXT_S,
    "marginBottom": "4px",
    "marginTop": "14px",
}
style_dropdown = {
    "backgroundColor": BG_PANEL,
    "borderColor": BORDER,
    "borderRadius": "6px",
    "color": TEXT_P,
    "fontSize": "12px",
}
style_kpi_row = {
    "display": "grid",
    "gridTemplateColumns": "repeat(auto-fill, minmax(150px, 1fr))",
    "gap": "12px",
    "marginBottom": "24px",
}
style_kpi_card = {
    "backgroundColor": BG_CARD,
    "border": f"1px solid {BORDER}",
    "borderTop": f"3px solid {ACCENT}",
    "borderRadius": "8px",
    "padding": "16px 14px",
    "textAlign": "center",
    "boxShadow": "0 2px 8px rgba(41,171,226,0.12)",
    "transition": "transform 0.2s, box-shadow 0.2s",
}
style_chart_row = {
    "display": "grid",
    "gap": "16px",
    "marginBottom": "16px",
}
style_chart_card = {
    "backgroundColor": BG_PANEL,
    "border": f"1px solid {BORDER}",
    "borderRadius": "8px",
    "padding": "4px 8px 8px",
    "boxShadow": "0 2px 8px rgba(41,171,226,0.08)",
}


def kpi_card(card_id: str, label: str, accent_color: str = ACCENT,
             icon: str = "") -> html.Div:
    """Create a KPI card component with a placeholder value."""
    return html.Div([
        html.Div(icon, style={"fontSize": "20px", "marginBottom": "4px"}),
        html.Div(id=f"kpi-{card_id}",
                 style={"fontSize": "26px", "fontWeight": "800",
                        "color": accent_color, "lineHeight": "1"}),
        html.Div(label, style={"fontSize": "10px", "color": TEXT_S,
                                "marginTop": "6px", "fontWeight": "700",
                                "textTransform": "uppercase",
                                "letterSpacing": "0.8px"}),
    ], style=style_kpi_card)


def chart_card(graph_id: str, height: int = 340) -> html.Div:
    """Wrap a dcc.Graph in a styled card."""
    return html.Div(
        dcc.Graph(id=graph_id, config={"displayModeBar": False},
                  style={"height": f"{height}px"}),
        style=style_chart_card,
    )


def make_dropdown(drop_id: str, options: list[dict], placeholder: str) -> dcc.Dropdown:
    return dcc.Dropdown(
        id=drop_id,
        options=options,
        multi=True,
        placeholder=placeholder,
        style=style_dropdown,
        className="dash-dropdown-dark",
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3.  LAYOUT
# ─────────────────────────────────────────────────────────────────────────────
app.layout = html.Div(style=style_page, children=[

    # ── Google Fonts ──────────────────────────────────────────────────────────
    html.Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap",
    ),

    # ── HEADER ────────────────────────────────────────────────────────────────
    html.Div(style=style_header, children=[
        html.Div("📊", style={"fontSize": "32px"}),
        html.Div([
            html.H1("Student Engagement & Performance Dashboard",
                    style={"margin": "0", "fontSize": "20px", "fontWeight": "800",
                           "color": "#FFFFFF", "letterSpacing": "0.3px"}),
            html.P("xAPI Education Dataset — Interactive Analytics",
                   style={"margin": "2px 0 0", "fontSize": "12px",
                          "color": "rgba(255,255,255,0.80)",
                          "letterSpacing": "0.5px"}),
        ]),
    ]),

    # ── BODY (sidebar + main) ─────────────────────────────────────────────────
    html.Div(style=style_body, children=[

        # ── SIDEBAR: FILTERS ──────────────────────────────────────────────────
        html.Div(style=style_sidebar, children=[
            html.Div([
                html.Span("🔍", style={"marginRight": "6px"}),
                html.Span("FILTERS"),
            ], style={
                "fontSize": "11px", "fontWeight": "800", "letterSpacing": "2px",
                "color": ACCENT, "marginBottom": "16px",
                "borderBottom": f"2px solid {ACCENT}", "paddingBottom": "8px",
                "display": "flex", "alignItems": "center",
            }),

            html.Div("Gender", style=style_label),
            make_dropdown("filter-gender",
                          unique_opts(df_global["gender"]),
                          "All Genders"),

            html.Div("Academic Stage", style=style_label),
            make_dropdown("filter-stage",
                          unique_opts(df_global["StageID"]),
                          "All Stages"),

            html.Div("Grade", style=style_label),
            make_dropdown("filter-grade",
                          unique_opts(df_global["GradeID"]),
                          "All Grades"),

            html.Div("Subject / Topic", style=style_label),
            make_dropdown("filter-topic",
                          unique_opts(df_global["Topic"]),
                          "All Topics"),

            html.Div("Semester", style=style_label),
            make_dropdown("filter-semester",
                          unique_opts(df_global["Semester"]),
                          "All Semesters"),

            html.Div("Parent Satisfaction", style=style_label),
            make_dropdown("filter-parent-satisfaction",
                          unique_opts(df_global["ParentschoolSatisfaction"]),
                          "All"),

            html.Div("Absence Category", style=style_label),
            make_dropdown("filter-absence",
                          unique_opts(df_global["StudentAbsenceDays"]),
                          "All"),

            # Reset button
            html.Button("↺  Reset Filters", id="btn-reset",
                        n_clicks=0,
                        style={
                            "marginTop": "22px", "width": "100%",
                            "padding": "9px", "borderRadius": "6px",
                            "background": f"linear-gradient(135deg, {ACCENT2}, #6aa832)",
                            "color": "#fff", "border": "none",
                            "fontWeight": "700", "fontSize": "12px",
                            "cursor": "pointer", "letterSpacing": "0.5px",
                            "boxShadow": f"0 2px 8px rgba(141,198,63,0.35)",
                        }),

            # Filtered record count
            html.Div(id="record-count",
                     style={"marginTop": "12px", "fontSize": "11px",
                            "color": TEXT_S, "textAlign": "center"}),
        ]),

        # ── MAIN CONTENT ──────────────────────────────────────────────────────
        html.Div(style=style_main, children=[

            # ── KPI CARDS ─────────────────────────────────────────────────────
            html.Div(["📊 ", "Key Performance Indicators"],
                     style=style_section_title),
            html.Div(style=style_kpi_row, children=[
                kpi_card("total",      "Total Students",        ACCENT,    "👥"),
                kpi_card("pct-high",   "% High Performers",     "#8DC63F", "🏆"),
                kpi_card("pct-med",    "% Medium Performers",   "#29ABE2", "📈"),
                kpi_card("pct-low",    "% Low Performers",      "#E05C5C", "⚠️"),
                kpi_card("avg-hands",  "Avg Raised Hands",      "#4472C4", "✋"),
                kpi_card("avg-res",    "Avg Resources Visited", "#8DC63F", "📚"),
                kpi_card("avg-disc",   "Avg Discussion",        "#29ABE2", "💬"),
            ]),

            # ── PERFORMANCE OVERVIEW ──────────────────────────────────────────
            html.Div(["🎯 ", "Performance Overview"],
                     style=style_section_title),
            html.Div(style={**style_chart_row,
                            "gridTemplateColumns": "1fr 1fr 1fr"}, children=[
                chart_card("chart-perf-pie",    360),
                chart_card("chart-perf-gender", 360),
                chart_card("chart-perf-stage",  360),
            ]),

            # ── ENGAGEMENT ANALYTICS ──────────────────────────────────────────
            html.Div(["📡 ", "Engagement Analytics"],
                     style=style_section_title),
            html.Div(style={**style_chart_row,
                            "gridTemplateColumns": "1fr 1fr"}, children=[
                chart_card("chart-hands-perf",  340),
                chart_card("chart-res-perf",    340),
            ]),
            html.Div(style={**style_chart_row,
                            "gridTemplateColumns": "1.4fr 1fr"}, children=[
                chart_card("chart-scatter",     380),
                chart_card("chart-box-disc",    380),
            ]),

            # ── ATTENDANCE & PARENT INSIGHTS ──────────────────────────────────
            html.Div(["🏫 ", "Attendance & Parent Insights"],
                     style=style_section_title),
            html.Div(style={**style_chart_row,
                            "gridTemplateColumns": "1fr 1fr 1fr"}, children=[
                chart_card("chart-absence-perf",      340),
                chart_card("chart-parent-sat-perf",   340),
                chart_card("chart-parent-survey-perf",340),
            ]),

            # ── DATA TABLE ────────────────────────────────────────────────────
            html.Div(["📋 ", "Filtered Student Records"],
                     style=style_section_title),
            html.Div(
                dash_table.DataTable(
                    id="data-table",
                    columns=[
                        {"name": c, "id": c, "deletable": False, "selectable": False}
                        for c in ["gender", "NationalITy", "StageID", "GradeID",
                                  "Topic", "Semester", "raisedhands",
                                  "VisITedResources", "AnnouncementsView",
                                  "Discussion", "ParentAnsweringSurvey",
                                  "ParentschoolSatisfaction",
                                  "StudentAbsenceDays", "Class"]
                    ],
                    page_size=20,
                    sort_action="native",
                    sort_mode="multi",
                    filter_action="none",
                    style_table={
                        "overflowX": "auto",
                        "borderRadius": "10px",
                        "border": f"1px solid {BORDER}",
                    },
                    style_header={
                        "backgroundColor": ACCENT,
                        "color": "#FFFFFF",
                        "fontWeight": "700",
                        "fontSize": "11px",
                        "textTransform": "uppercase",
                        "letterSpacing": "0.8px",
                        "border": f"1px solid {BORDER}",
                    },
                    style_cell={
                        "backgroundColor": BG_PANEL,
                        "color": TEXT_P,
                        "border": f"1px solid {BORDER}",
                        "fontSize": "12px",
                        "padding": "8px 12px",
                        "fontFamily": FONT,
                        "textAlign": "left",
                        "whiteSpace": "normal",
                        "height": "auto",
                    },
                    style_data_conditional=[
                        {"if": {"filter_query": '{Class} = "High"'},
                         "color": "#6AA832", "fontWeight": "700"},
                        {"if": {"filter_query": '{Class} = "Medium"'},
                         "color": "#1A88BB", "fontWeight": "700"},
                        {"if": {"filter_query": '{Class} = "Low"'},
                         "color": "#C0392B", "fontWeight": "700"},
                        {"if": {"row_index": "odd"},
                         "backgroundColor": "#F7FBFE"},
                        {"if": {"state": "selected"},
                         "backgroundColor": "#D6EAF8",
                         "border": f"1px solid {ACCENT}"},
                    ],
                ),
                style={"borderRadius": "10px", "overflow": "hidden"},
            ),

        ]),  # end main
    ]),  # end body
])  # end layout


# ─────────────────────────────────────────────────────────────────────────────
# 4.  HELPER — apply filter mask
# ─────────────────────────────────────────────────────────────────────────────
def apply_filters(gender, stage, grade, topic, semester,
                  parent_sat, absence) -> pd.DataFrame:
    """Return a filtered copy of df_global based on dropdown selections."""
    dff = df_global.copy()
    if gender:
        dff = dff[dff["gender"].isin(gender)]
    if stage:
        dff = dff[dff["StageID"].isin(stage)]
    if grade:
        dff = dff[dff["GradeID"].isin(grade)]
    if topic:
        dff = dff[dff["Topic"].isin(topic)]
    if semester:
        dff = dff[dff["Semester"].isin(semester)]
    if parent_sat:
        dff = dff[dff["ParentschoolSatisfaction"].isin(parent_sat)]
    if absence:
        dff = dff[dff["StudentAbsenceDays"].isin(absence)]
    return dff


def empty_fig(message: str = "No data available for the selected filters.") -> go.Figure:
    """Return a styled empty figure with a centered annotation."""
    fig = go.Figure()
    fig.add_annotation(
        text=message, x=0.5, y=0.5,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(color=TEXT_S, size=14, family=FONT),
    )
    fig.update_layout(**PLOT_LAYOUT)
    return fig


def apply_theme(fig: go.Figure) -> go.Figure:
    """Apply the dark theme to any Plotly figure."""
    fig.update_layout(**PLOT_LAYOUT)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# 5.  RESET CALLBACK
# ─────────────────────────────────────────────────────────────────────────────
@app.callback(
    Output("filter-gender", "value"),
    Output("filter-stage", "value"),
    Output("filter-grade", "value"),
    Output("filter-topic", "value"),
    Output("filter-semester", "value"),
    Output("filter-parent-satisfaction", "value"),
    Output("filter-absence", "value"),
    Input("btn-reset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(_):
    """Clear all filter dropdowns on Reset click."""
    return None, None, None, None, None, None, None


# ─────────────────────────────────────────────────────────────────────────────
# 6.  MAIN CALLBACK — all charts + KPIs + table
# ─────────────────────────────────────────────────────────────────────────────
@app.callback(
    # KPIs
    Output("kpi-total",     "children"),
    Output("kpi-pct-high",  "children"),
    Output("kpi-pct-med",   "children"),
    Output("kpi-pct-low",   "children"),
    Output("kpi-avg-hands", "children"),
    Output("kpi-avg-res",   "children"),
    Output("kpi-avg-disc",  "children"),
    # Charts — Performance Overview
    Output("chart-perf-pie",    "figure"),
    Output("chart-perf-gender", "figure"),
    Output("chart-perf-stage",  "figure"),
    # Charts — Engagement
    Output("chart-hands-perf",  "figure"),
    Output("chart-res-perf",    "figure"),
    Output("chart-scatter",     "figure"),
    Output("chart-box-disc",    "figure"),
    # Charts — Attendance & Parent
    Output("chart-absence-perf",       "figure"),
    Output("chart-parent-sat-perf",    "figure"),
    Output("chart-parent-survey-perf", "figure"),
    # DataTable + record count
    Output("data-table",    "data"),
    Output("record-count",  "children"),
    # Filters
    Input("filter-gender",              "value"),
    Input("filter-stage",               "value"),
    Input("filter-grade",               "value"),
    Input("filter-topic",               "value"),
    Input("filter-semester",            "value"),
    Input("filter-parent-satisfaction", "value"),
    Input("filter-absence",             "value"),
)
def update_dashboard(gender, stage, grade, topic, semester,
                     parent_sat, absence):
    """Single master callback — updates every output when any filter changes."""

    dff = apply_filters(gender, stage, grade, topic, semester, parent_sat, absence)
    total = len(dff)

    # ── Empty-state guard ──────────────────────────────────────────────────
    if total == 0:
        empty = empty_fig()
        kpi_na = "—"
        return (
            kpi_na, kpi_na, kpi_na, kpi_na, kpi_na, kpi_na, kpi_na,
            empty, empty, empty, empty, empty, empty, empty,
            empty, empty, empty,
            [], "⚠️ No records match the selected filters.",
        )

    # ── KPIs ───────────────────────────────────────────────────────────────
    vc = dff["Class"].value_counts()
    pct_high = f"{vc.get('High', 0) / total * 100:.1f}%"
    pct_med  = f"{vc.get('Medium', 0) / total * 100:.1f}%"
    pct_low  = f"{vc.get('Low', 0) / total * 100:.1f}%"
    avg_hands = f"{dff['raisedhands'].mean():.1f}"
    avg_res   = f"{dff['VisITedResources'].mean():.1f}"
    avg_disc  = f"{dff['Discussion'].mean():.1f}"

    # ── A) Performance Overview ────────────────────────────────────────────

    # Pie chart: performance distribution
    perf_counts = (dff["Class"].value_counts()
                       .reindex(PERF_ORDER).fillna(0).reset_index())
    perf_counts.columns = ["Class", "Count"]
    fig_pie = px.pie(
        perf_counts, names="Class", values="Count",
        color="Class", color_discrete_map=PERF_COLORS,
        title="Performance Distribution",
        hole=0.42,
    )
    fig_pie.update_traces(
        textposition="outside",
        textinfo="percent+label",
        textfont=dict(size=12, color=TEXT_P),
        marker=dict(line=dict(color=BG_APP, width=2)),
    )
    apply_theme(fig_pie)

    # Bar: performance by gender
    perf_gender = (dff.groupby(["gender", "Class"], observed=True)
                      .size().reset_index(name="Count"))
    fig_gender = px.bar(
        perf_gender, x="gender", y="Count", color="Class",
        color_discrete_map=PERF_COLORS,
        barmode="group", title="Performance by Gender",
        category_orders={"Class": PERF_ORDER},
        labels={"gender": "Gender", "Count": "Students"},
    )
    apply_theme(fig_gender)

    # Bar: performance by stage
    perf_stage = (dff.groupby(["StageID", "Class"], observed=True)
                     .size().reset_index(name="Count"))
    fig_stage = px.bar(
        perf_stage, x="StageID", y="Count", color="Class",
        color_discrete_map=PERF_COLORS,
        barmode="group", title="Performance by Academic Stage",
        category_orders={"Class": PERF_ORDER},
        labels={"StageID": "Stage", "Count": "Students"},
    )
    apply_theme(fig_stage)

    # ── B) Engagement Analytics ────────────────────────────────────────────

    # Bar: avg raised hands by performance
    hands_perf = (dff.groupby("Class", observed=True)["raisedhands"]
                     .mean().reindex(PERF_ORDER).reset_index())
    hands_perf.columns = ["Class", "Avg Raised Hands"]
    fig_hands = px.bar(
        hands_perf, x="Class", y="Avg Raised Hands", color="Class",
        color_discrete_map=PERF_COLORS,
        title="Avg Raised Hands by Performance",
        text_auto=".1f",
        category_orders={"Class": PERF_ORDER},
    )
    fig_hands.update_traces(textposition="outside",
                            textfont=dict(color=TEXT_P))
    apply_theme(fig_hands)

    # Bar: avg resources visited by performance
    res_perf = (dff.groupby("Class", observed=True)["VisITedResources"]
                   .mean().reindex(PERF_ORDER).reset_index())
    res_perf.columns = ["Class", "Avg Resources Visited"]
    fig_res = px.bar(
        res_perf, x="Class", y="Avg Resources Visited", color="Class",
        color_discrete_map=PERF_COLORS,
        title="Avg Resources Visited by Performance",
        text_auto=".1f",
        category_orders={"Class": PERF_ORDER},
    )
    fig_res.update_traces(textposition="outside",
                          textfont=dict(color=TEXT_P))
    apply_theme(fig_res)

    # Scatter: raised hands vs visited resources (color = performance)
    fig_scatter = px.scatter(
        dff, x="raisedhands", y="VisITedResources",
        color="Class", color_discrete_map=PERF_COLORS,
        title="Raised Hands vs Visited Resources",
        labels={"raisedhands": "Raised Hands",
                "VisITedResources": "Visited Resources"},
        opacity=0.75,
        category_orders={"Class": PERF_ORDER},
    )
    fig_scatter.update_traces(marker=dict(size=7, line=dict(width=0.4,
                                                             color="rgba(0,0,0,0.4)")))
    apply_theme(fig_scatter)

    # Box: discussion participation by performance
    fig_box = px.box(
        dff, x="Class", y="Discussion",
        color="Class", color_discrete_map=PERF_COLORS,
        title="Discussion Participation by Performance",
        labels={"Discussion": "Discussion Score", "Class": "Performance"},
        category_orders={"Class": PERF_ORDER},
        points="outliers",
    )
    apply_theme(fig_box)

    # ── C) Attendance & Parent Insights ────────────────────────────────────

    # Bar: absence category vs performance
    absence_perf = (dff.groupby(["StudentAbsenceDays", "Class"], observed=True)
                       .size().reset_index(name="Count"))
    fig_absence = px.bar(
        absence_perf, x="StudentAbsenceDays", y="Count", color="Class",
        color_discrete_map=PERF_COLORS,
        barmode="group", title="Absence Category vs Performance",
        labels={"StudentAbsenceDays": "Absence", "Count": "Students"},
        category_orders={"Class": PERF_ORDER},
    )
    apply_theme(fig_absence)

    # Bar: parent satisfaction vs performance
    sat_perf = (dff.groupby(["ParentschoolSatisfaction", "Class"], observed=True)
                   .size().reset_index(name="Count"))
    fig_sat = px.bar(
        sat_perf, x="ParentschoolSatisfaction", y="Count", color="Class",
        color_discrete_map=PERF_COLORS,
        barmode="group", title="Parent Satisfaction vs Performance",
        labels={"ParentschoolSatisfaction": "Satisfaction", "Count": "Students"},
        category_orders={"Class": PERF_ORDER},
    )
    apply_theme(fig_sat)

    # Bar: parent survey response vs performance
    survey_perf = (dff.groupby(["ParentAnsweringSurvey", "Class"], observed=True)
                      .size().reset_index(name="Count"))
    fig_survey = px.bar(
        survey_perf, x="ParentAnsweringSurvey", y="Count", color="Class",
        color_discrete_map=PERF_COLORS,
        barmode="group", title="Parent Survey Response vs Performance",
        labels={"ParentAnsweringSurvey": "Survey Response", "Count": "Students"},
        category_orders={"Class": PERF_ORDER},
    )
    apply_theme(fig_survey)

    # ── DataTable ──────────────────────────────────────────────────────────
    table_cols = ["gender", "NationalITy", "StageID", "GradeID", "Topic",
                  "Semester", "raisedhands", "VisITedResources",
                  "AnnouncementsView", "Discussion", "ParentAnsweringSurvey",
                  "ParentschoolSatisfaction", "StudentAbsenceDays", "Class"]
    table_data = dff[table_cols].to_dict("records")

    record_label = f"Showing {total:,} record{'s' if total != 1 else ''}"

    return (
        str(total), pct_high, pct_med, pct_low,
        avg_hands, avg_res, avg_disc,
        fig_pie, fig_gender, fig_stage,
        fig_hands, fig_res, fig_scatter, fig_box,
        fig_absence, fig_sat, fig_survey,
        table_data, record_label,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 7.  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("─" * 60)
    print("  Student Analytics Dashboard")
    print("  → http://127.0.0.1:8050")
    print("─" * 60)
    app.run(debug=True, host="127.0.0.1", port=8050)
