import streamlit as st
import pandas as pd
import plotly.express as px

from utils import call_api

st.title("⚠ Pressure Anomaly Detection")

st.markdown("---")

# -------------------------------------------------------
# Check Upload
# -------------------------------------------------------

if "uploaded_file" not in st.session_state:

    st.warning("Please upload a dataset from the Home page.")

    st.stop()

uploaded_file = st.session_state["uploaded_file"]

# -------------------------------------------------------
# Call Flask API
# -------------------------------------------------------

with st.spinner("Running Isolation Forest..."):

    result = call_api(
        "detect-pressure",
        uploaded_file
    )

# -------------------------------------------------------
# Error Handling
# -------------------------------------------------------

if result["status"] == "error":

    st.error(result["message"])

    st.stop()

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Pressure Anomalies",
    result["pressure_anomalies"]
)

col2.metric(
    "Average Score",
    f"{result['average_pressure_score']:.4f}"
)

col3.metric(
    "Records",
    result["records_processed"]
)

st.markdown("---")

# -------------------------------------------------------
# Pressure Score Cards
# -------------------------------------------------------

score_df = pd.DataFrame({

    "Metric":[

        "Maximum Score",

        "Average Score",

        "Minimum Score"

    ],

    "Value":[

        result["maximum_pressure_score"],

        result["average_pressure_score"],

        result["minimum_pressure_score"]

    ]

})

st.subheader("Pressure Score Summary")

st.dataframe(
    score_df,
    use_container_width=True
)

# -------------------------------------------------------
# Bar Chart
# -------------------------------------------------------

fig = px.bar(

    score_df,

    x="Metric",

    y="Value",

    title="Pressure Score Statistics",

    text_auto=".3f"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Gauge Indicator
# -------------------------------------------------------

gauge = px.pie(

    names=["Normal","Anomaly"],

    values=[
        result["records_processed"]-
        result["pressure_anomalies"],

        result["pressure_anomalies"]

    ],

    title="Pressure Status Distribution"

)

st.plotly_chart(
    gauge,
    use_container_width=True
)