from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

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
PERF_COLORS = {"High": "#8DC63F", "Medium": "#29ABE2", "Low": "#E05C5C"}

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")
    df.dropna(subset=["Class", "gender", "StageID"], inplace=True)
    df["Class"] = df["Class"].map(CLASS_MAP).fillna(df["Class"])
    df["Class"] = pd.Categorical(df["Class"], categories=PERF_ORDER, ordered=True)
    df["Semester"] = df["Semester"].replace({"F": "First", "S": "Second"})
    for col in ["raisedhands", "VisITedResources", "AnnouncementsView", "Discussion"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df

df_global = load_data(CSV_PATH)

def apply_filters(filters: dict) -> pd.DataFrame:
    dff = df_global.copy()
    if filters.get("gender"):
        dff = dff[dff["gender"].isin(filters["gender"])]
    if filters.get("stage"):
        dff = dff[dff["StageID"].isin(filters["stage"])]
    if filters.get("grade"):
        dff = dff[dff["GradeID"].isin(filters["grade"])]
    if filters.get("topic"):
        dff = dff[dff["Topic"].isin(filters["topic"])]
    if filters.get("semester"):
        dff = dff[dff["Semester"].isin(filters["semester"])]
    if filters.get("parent_sat"):
        dff = dff[dff["ParentschoolSatisfaction"].isin(filters["parent_sat"])]
    if filters.get("absence"):
        dff = dff[dff["StudentAbsenceDays"].isin(filters["absence"])]
    return dff

@app.route("/api/dashboard", methods=["POST"])
def get_dashboard_data():
    filters = request.json or {}
    dff = apply_filters(filters)
    total = len(dff)

    if total == 0:
        return jsonify({
            "kpis": {
                "total": 0, "pct_high": "0%", "pct_med": "0%", "pct_low": "0%",
                "avg_hands": "0", "avg_res": "0", "avg_disc": "0"
            },
            "charts": {},
            "tableData": [],
            "countLabel": "Showing 0 records"
        })

    # KPIs
    vc = dff["Class"].value_counts()
    kpis = {
        "total": total,
        "pct_high": f"{vc.get('High', 0) / total * 100:.1f}%",
        "pct_med": f"{vc.get('Medium', 0) / total * 100:.1f}%",
        "pct_low": f"{vc.get('Low', 0) / total * 100:.1f}%",
        "avg_hands": f"{dff['raisedhands'].mean():.1f}",
        "avg_res": f"{dff['VisITedResources'].mean():.1f}",
        "avg_disc": f"{dff['Discussion'].mean():.1f}"
    }

    # Helper to convert plotly express figure to dict
    def fig_to_dict(fig):
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="'Inter', sans-serif", color="#2D3748", size=12),
            margin=dict(l=40, r=20, t=40, b=40)
        )
        return json.loads(json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder))

    charts = {}

    # Performance Distribution
    perf_counts = dff["Class"].value_counts().reindex(PERF_ORDER).fillna(0).reset_index()
    perf_counts.columns = ["Class", "Count"]
    fig_pie = px.pie(perf_counts, names="Class", values="Count", color="Class", 
                     color_discrete_map=PERF_COLORS, hole=0.42, title="Performance Distribution")
    charts["perf_pie"] = fig_to_dict(fig_pie)

    # Performance by Gender
    perf_gender = dff.groupby(["gender", "Class"], observed=True).size().reset_index(name="Count")
    fig_gender = px.bar(perf_gender, x="gender", y="Count", color="Class", 
                        color_discrete_map=PERF_COLORS, barmode="group", title="Performance by Gender")
    charts["perf_gender"] = fig_to_dict(fig_gender)

    # Performance by Stage
    perf_stage = dff.groupby(["StageID", "Class"], observed=True).size().reset_index(name="Count")
    fig_stage = px.bar(perf_stage, x="StageID", y="Count", color="Class", 
                       color_discrete_map=PERF_COLORS, barmode="group", title="Performance by Academic Stage")
    charts["perf_stage"] = fig_to_dict(fig_stage)

    # Engagement
    hands_perf = dff.groupby("Class", observed=True)["raisedhands"].mean().reindex(PERF_ORDER).reset_index()
    fig_hands = px.bar(hands_perf, x="Class", y="raisedhands", color="Class", color_discrete_map=PERF_COLORS, 
                       title="Avg Raised Hands by Performance", text_auto=".1f")
    charts["hands_perf"] = fig_to_dict(fig_hands)

    res_perf = dff.groupby("Class", observed=True)["VisITedResources"].mean().reindex(PERF_ORDER).reset_index()
    fig_res = px.bar(res_perf, x="Class", y="VisITedResources", color="Class", color_discrete_map=PERF_COLORS, 
                     title="Avg Resources Visited by Performance", text_auto=".1f")
    charts["res_perf"] = fig_to_dict(fig_res)

    fig_scatter = px.scatter(dff, x="raisedhands", y="VisITedResources", color="Class", 
                             color_discrete_map=PERF_COLORS, title="Raised Hands vs Visited Resources")
    charts["scatter"] = fig_to_dict(fig_scatter)

    fig_box = px.box(dff, x="Class", y="Discussion", color="Class", color_discrete_map=PERF_COLORS, 
                     title="Discussion Participation by Performance")
    charts["box_disc"] = fig_to_dict(fig_box)

    # Attendance & Parent
    absence_perf = dff.groupby(["StudentAbsenceDays", "Class"], observed=True).size().reset_index(name="Count")
    fig_absence = px.bar(absence_perf, x="StudentAbsenceDays", y="Count", color="Class", 
                         color_discrete_map=PERF_COLORS, barmode="group", title="Absence Category vs Performance")
    charts["absence_perf"] = fig_to_dict(fig_absence)

    sat_perf = dff.groupby(["ParentschoolSatisfaction", "Class"], observed=True).size().reset_index(name="Count")
    fig_sat = px.bar(sat_perf, x="ParentschoolSatisfaction", y="Count", color="Class", 
                     color_discrete_map=PERF_COLORS, barmode="group", title="Parent Satisfaction vs Performance")
    charts["sat_perf"] = fig_to_dict(fig_sat)

    survey_perf = dff.groupby(["ParentAnsweringSurvey", "Class"], observed=True).size().reset_index(name="Count")
    fig_survey = px.bar(survey_perf, x="ParentAnsweringSurvey", y="Count", color="Class", 
                        color_discrete_map=PERF_COLORS, barmode="group", title="Parent Survey Response vs Performance")
    charts["survey_perf"] = fig_to_dict(fig_survey)

    # Table Data
    table_cols = ["gender", "NationalITy", "StageID", "GradeID", "Topic", "Semester", "raisedhands", 
                  "VisITedResources", "AnnouncementsView", "Discussion", "ParentAnsweringSurvey", 
                  "ParentschoolSatisfaction", "StudentAbsenceDays", "Class"]
    table_data = dff[table_cols].to_dict("records")

    # Options for filters
    options = {
        "gender": sorted(df_global["gender"].unique().tolist()),
        "stage": sorted(df_global["StageID"].unique().tolist()),
        "grade": sorted(df_global["GradeID"].unique().tolist()),
        "topic": sorted(df_global["Topic"].unique().tolist()),
        "semester": sorted(df_global["Semester"].unique().tolist()),
        "parent_sat": sorted(df_global["ParentschoolSatisfaction"].unique().tolist()),
        "absence": sorted(df_global["StudentAbsenceDays"].unique().tolist())
    }

    return jsonify({
        "kpis": kpis,
        "charts": charts,
        "tableData": table_data,
        "options": options,
        "countLabel": f"Showing {total:,} records"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
