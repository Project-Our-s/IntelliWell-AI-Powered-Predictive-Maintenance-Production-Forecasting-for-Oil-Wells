import streamlit as st
import plotly.graph_objects as go

from utils import call_api

st.title("❤️ Well Health Assessment")

st.markdown("---")

# =====================================================
# Check Upload
# =====================================================

if "uploaded_file" not in st.session_state:

    st.warning("Please upload a dataset from the Home page.")

    st.stop()

uploaded_file = st.session_state["uploaded_file"]

# =====================================================
# Call Flask API
# =====================================================

with st.spinner("Calculating Well Health..."):

    result = call_api(
        "well-health",
        uploaded_file
    )

# =====================================================
# Error Handling
# =====================================================

if result["status"] == "error":

    st.error(result["message"])

    st.stop()

# =====================================================
# KPI Cards
# =====================================================

col1, col2, col3 = st.columns(3)

col1.metric(

    "Average Health Score",

    f"{result['average_health_score']:.2f}"

)

col2.metric(

    "Maximum Health Score",

    f"{result['maximum_health_score']:.2f}"

)

col3.metric(

    "Minimum Health Score",

    f"{result['minimum_health_score']:.2f}"

)

st.markdown("---")

# =====================================================
# Health Gauge
# =====================================================

health = result["average_health_score"]

fig = go.Figure(go.Indicator(

    mode="gauge+number",

    value=health,

    title={"text":"Overall Well Health"},

    gauge={

        "axis":{"range":[0,100]},

        "bar":{"color":"darkgreen"},

        "steps":[

            {"range":[0,50],"color":"red"},

            {"range":[50,70],"color":"orange"},

            {"range":[70,85],"color":"yellow"},

            {"range":[85,100],"color":"lightgreen"}

        ]

    }

))

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================================
# Health Status
# =====================================================

if health >= 85:

    st.success("🟢 Operational Status : Healthy")

elif health >= 70:

    st.warning("🟡 Operational Status : Monitor")

elif health >= 50:

    st.warning("🟠 Operational Status : Warning")

else:

    st.error("🔴 Operational Status : Critical")

st.markdown("---")

# =====================================================
# Recommendation
# =====================================================

if health >= 85:

    st.success(
        "Continue normal production. No immediate action required."
    )

elif health >= 70:

    st.info(
        "Increase monitoring frequency."
    )

elif health >= 50:

    st.warning(
        "Inspect pressure system and choke settings."
    )

else:

    st.error(
        "Immediate maintenance recommended. Inspect tubing, sensors and production equipment."
    )