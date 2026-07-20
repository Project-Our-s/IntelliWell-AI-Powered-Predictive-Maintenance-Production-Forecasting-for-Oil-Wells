import streamlit as st
import pandas as pd
import plotly.express as px

from utils import call_api

st.title("📈 Production Forecast")

st.markdown("---")

# --------------------------------------------------
# Check Upload
# --------------------------------------------------

if "uploaded_file" not in st.session_state:

    st.warning("Please upload a dataset from the Home page.")

    st.stop()

uploaded_file = st.session_state["uploaded_file"]

# --------------------------------------------------
# API Call
# --------------------------------------------------

with st.spinner("Running Random Forest Model..."):

    result = call_api(
        "predict-production",
        uploaded_file
    )

# --------------------------------------------------
# Error Handling
# --------------------------------------------------

if result["status"] == "error":

    st.error(result["message"])

    st.stop()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Prediction",
    f"{result['average_prediction']:.2f}"
)

col2.metric(
    "Maximum Prediction",
    f"{result['maximum_prediction']:.2f}"
)

col3.metric(
    "Minimum Prediction",
    f"{result['minimum_prediction']:.2f}"
)

st.markdown("---")

# --------------------------------------------------
# Prediction Table
# --------------------------------------------------

prediction_df = pd.DataFrame(
    result["predictions"]
)

st.subheader("Predicted Production")

st.dataframe(
    prediction_df,
    use_container_width=True
)

# --------------------------------------------------
# Plot
# --------------------------------------------------

fig = px.line(

    prediction_df,

    y="Predicted Production",

    title="Predicted Production"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Histogram
# --------------------------------------------------

fig2 = px.histogram(

    prediction_df,

    x="Predicted Production",

    nbins=20,

    title="Prediction Distribution"

)

st.plotly_chart(
    fig2,
    use_container_width=True
)