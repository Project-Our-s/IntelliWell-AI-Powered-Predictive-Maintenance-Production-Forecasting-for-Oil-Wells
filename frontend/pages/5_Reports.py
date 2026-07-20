import streamlit as st
from pathlib import Path
import os

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="IntelliWell Report Center",
    page_icon="📄",
    layout="wide"
)

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================================
# Report Files
# ==========================================================

REPORTS = {
    "📊 Executive Summary":
        PROJECT_ROOT / "Executive_Summary.csv",

    "⛽ Production Forecast":
        PROJECT_ROOT / "production_forecast_results.csv",

    "⚠ Pressure Analysis":
        PROJECT_ROOT / "pressure_anomaly_results.csv",

    "❤️ Well Health Report":
        PROJECT_ROOT / "well_health_results.csv",

    "📈 Future Forecast":
        PROJECT_ROOT / "future_forecast.csv",

    "📋 Final IntelliWell Report":
        PROJECT_ROOT / "IntelliWell_Final_Report.csv"
}

# ==========================================================
# Page Title
# ==========================================================

st.title("📄 IntelliWell Report Center")

st.caption(
    "Download AI-generated reports and prediction results."
)

st.markdown("---")

# ==========================================================
# Report Statistics
# ==========================================================

available_reports = sum(
    file.exists()
    for file in REPORTS.values()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Reports Available",
        f"{available_reports}/6"
    )

with col2:
    st.metric(
        "ML Models",
        "2"
    )

with col3:
    st.metric(
        "Forecast Horizon",
        "365 Days"
    )

with col4:
    if available_reports == 6:
        st.metric(
            "Status",
            "Ready ✅"
        )
    else:
        st.metric(
            "Status",
            "Partial ⚠"
        )

st.markdown("---")

# ==========================================================
# Download Section
# ==========================================================

st.subheader("📥 Download AI Generated Reports")

left, right = st.columns(2)

report_items = list(REPORTS.items())

for i, (title, filepath) in enumerate(report_items):

    column = left if i % 2 == 0 else right

    with column:

        if filepath.exists():

            st.success(f"✅ {title}")

            st.caption(
                f"File: {filepath.name}"
            )

            st.caption(
                f"Size: {filepath.stat().st_size / 1024:.1f} KB"
            )

            st.caption(
                "Status: Ready for download"
            )

            with open(filepath, "rb") as file:

                st.download_button(
                    label=f"⬇ Download {title}",
                    data=file,
                    file_name=filepath.name,
                    mime="text/csv",
                    use_container_width=True
                )

        else:

            st.error(
                f"❌ {filepath.name} not found."
            )

st.markdown("---")

# ==========================================================
# AI Summary
# ==========================================================

st.subheader("🤖 AI Summary")

st.info(
"""
### IntelliWell AI Report Summary

The IntelliWell system has successfully generated reports for:

- 📊 Executive Overview
- ⛽ Production Forecasting
- ⚠ Pressure Anomaly Detection
- ❤️ Well Health Assessment
- 📈 Future Forecast Simulation
- 📋 Final AI Report

These reports can be downloaded for:

- Executive decision making
- Maintenance planning
- Production optimization
- Risk assessment
- Technical documentation
- Final project presentation
"""
)

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

if available_reports == 6:

    st.success(
"""
✅ **All reports are available and ready for download.**

Thank you for using **IntelliWell – AI Powered Predictive Maintenance System**.
"""
    )

else:

    st.warning(
f"""
Only **{available_reports}** of **6** reports are currently available.

Please generate the missing reports before downloading.
"""
    )