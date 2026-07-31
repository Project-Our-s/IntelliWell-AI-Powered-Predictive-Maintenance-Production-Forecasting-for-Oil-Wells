import streamlit as st
import pandas as pd
import os
import sys

import re

def safe_filename(name):

    return re.sub(

        r'[<>:"/\\\\|?*]',

        "_",

        str(name)

    )
# ==========================================================
# Backend Path
# ==========================================================

BACKEND_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "backend"
    )
)

sys.path.append(BACKEND_PATH)

from ai_engine import (
    generate_ai_summary,
    generate_alerts,
    generate_action_plan
)

from pdf_generator import create_pdf_report

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="AI Executive Report",
    page_icon="📄",
    layout="wide"
)

st.title("📄 IntelliWell AI Executive Report")

st.markdown(
"""
Generate a professional AI executive report
for any forecasted well.
"""
)

# ==========================================================
# Load Forecast Dataset
# ==========================================================

CSV_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "future_forecast.csv"
    )
)

df = pd.read_csv(CSV_PATH)

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("Report Settings")

selected_well = st.sidebar.selectbox(
    "Select Well",
    sorted(df["NPD_WELL_BORE_NAME"].unique())
)

well_df = df[
    df["NPD_WELL_BORE_NAME"] == selected_well
]

forecast_day = st.sidebar.selectbox(
    "Forecast Horizon",
    sorted(well_df["Forecast Days"].unique())
)

row = well_df[
    well_df["Forecast Days"] == forecast_day
].iloc[0].copy()

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("Prediction Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Production",
    f"{row['Predicted Production']:.2f}"
)

c2.metric(
    "Health",
    f"{row['Well Health Score']:.2f}%"
)

c3.metric(
    "Pressure",
    row["Pressure Status"]
)

c4.metric(
    "Confidence",
    f"{row['Forecast Confidence (%)']:.2f}%"
)

st.divider()

# ==========================================================
# AI Processing
# ==========================================================

ai_input = {

    "Predicted Production":
        float(row["Predicted Production"]),

    "Well Health Score":
        float(row["Well Health Score"]),

    "Pressure Status":
        row["Pressure Status"],

    "Expected Anomaly":
        int(row["Expected Anomaly"]),

    "Recommendation":
        row["Recommendation"],

    "Forecast Confidence (%)":
        float(row["Forecast Confidence (%)"])

}

summary = generate_ai_summary(ai_input)

alerts = generate_alerts(ai_input)

action_plan = generate_action_plan(ai_input)

row["AI Summary"] = summary["summary"]

row["Smart Alerts"] = "\n".join(alerts)

row["Action Plan"] = "\n".join(action_plan)

# ==========================================================
# AI Executive Summary
# ==========================================================

st.subheader("🤖 AI Executive Summary")

st.info(row["AI Summary"])

# ==========================================================
# Smart Alerts
# ==========================================================

st.subheader("🚨 Smart Alerts")

for alert in alerts:

    st.warning(alert)

# ==========================================================
# Action Plan
# ==========================================================

st.subheader("🛠 AI Action Plan")

for action in action_plan:

    st.markdown(f"- {action}")

st.divider()

# ==========================================================
# Generate Report
# ==========================================================

if st.button(
    "📄 Generate Executive Report",
    use_container_width=True
):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    pdf_path = create_pdf_report(

        row,

        f"reports/{safe_filename(selected_well)}_{forecast_day}_Days_Report.pdf"


    )

    st.success("✅ AI Executive Report Generated Successfully!")

    with open(pdf_path, "rb") as pdf:

        st.download_button(

            label="⬇ Download PDF Report",

            data=pdf,

            file_name=os.path.basename(pdf_path),

            mime="application/pdf",

            use_container_width=True

        )

st.divider()

# ==========================================================
# Raw Prediction Data
# ==========================================================

with st.expander("📊 View Prediction Data"):

    st.dataframe(
        pd.DataFrame([row]),
        use_container_width=True
    )