import streamlit as st

st.set_page_config(

    page_title="IntelliWell",

    page_icon="🛢️",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ---------------------------------------------------

st.title("🛢️ IntelliWell")

st.subheader(
    "AI-Powered Oil Well Decision Support System"
)

st.markdown("---")

st.markdown(
"""
Welcome to **IntelliWell**.

This application integrates

- 📈 Production Forecasting
- ⚠ Pressure Anomaly Detection
- ❤️ Well Health Assessment
- 📊 Executive Dashboard
- 📄 Report Generation

using Machine Learning.
"""
)

st.markdown("---")

uploaded_file = st.file_uploader(

    "Upload Production Dataset",

    type=["xlsx","csv"]

)

if uploaded_file is not None:

    st.success("Dataset Uploaded Successfully.")

    st.session_state["uploaded_file"] = uploaded_file

    df = None

    if uploaded_file.name.endswith(".xlsx"):

        import pandas as pd

        df = pd.read_excel(uploaded_file)

    else:

        import pandas as pd

        df = pd.read_csv(uploaded_file)

    st.dataframe(df.head())