import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils import call_api

st.set_page_config(layout="wide")

st.title("📊 IntelliWell Executive Dashboard")

st.markdown("---")

# =====================================================
# Check Upload
# =====================================================

if "uploaded_file" not in st.session_state:

    st.warning("Please upload a dataset from the Home page.")

    st.stop()

uploaded_file = st.session_state["uploaded_file"]

# =====================================================
# API Call
# =====================================================

with st.spinner("Generating Executive Dashboard..."):

    dashboard = call_api(
        "dashboard-summary",
        uploaded_file
    )

# =====================================================
# Error Handling
# =====================================================

if dashboard["status"] == "error":

    st.error(dashboard["message"])

    st.stop()

# =====================================================
# KPI Row
# =====================================================

col1,col2,col3,col4 = st.columns(4)

col1.metric(

    "Predicted Production",

    f"{dashboard['average_predicted_production']:.2f}"

)

col2.metric(

    "Health Score",

    f"{dashboard['average_health_score']:.2f}"

)

col3.metric(

    "Pressure Anomalies",

    dashboard["pressure_anomalies"]

)

col4.metric(

    "Records",

    dashboard["records_processed"]

)

st.markdown("---")

# =====================================================
# Operational Status
# =====================================================

status_df = {

    "Status":[

        "Healthy",

        "Monitor",

        "Warning",

        "Critical"

    ],

    "Count":[

        dashboard["healthy"],

        dashboard["monitor"],

        dashboard["warning"],

        dashboard["critical"]

    ]

}

status_df = px.data.tips().iloc[:0]

import pandas as pd

status_df = pd.DataFrame({

    "Status":[

        "Healthy",

        "Monitor",

        "Warning",

        "Critical"

    ],

    "Count":[

        dashboard["healthy"],

        dashboard["monitor"],

        dashboard["warning"],

        dashboard["critical"]

    ]

})

# =====================================================
# Pie Chart
# =====================================================

pie = px.pie(

    status_df,

    names="Status",

    values="Count",

    hole=.5,

    title="Operational Status"

)

st.plotly_chart(

    pie,

    use_container_width=True

)

# =====================================================
# Bar Chart
# =====================================================

bar = px.bar(

    status_df,

    x="Status",

    y="Count",

    text="Count",

    title="Well Status Distribution"

)

st.plotly_chart(

    bar,

    use_container_width=True

)

# =====================================================
# Health Gauge
# =====================================================

fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=dashboard["average_health_score"],

        title={"text":"Average Well Health"},

        gauge={

            "axis":{"range":[0,100]},

            "bar":{"color":"green"},

            "steps":[

                {"range":[0,50],"color":"red"},

                {"range":[50,70],"color":"orange"},

                {"range":[70,85],"color":"yellow"},

                {"range":[85,100],"color":"lightgreen"}

            ]

        }

    )

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================================
# Executive Summary
# =====================================================

st.markdown("---")

st.subheader("Executive Summary")

if dashboard["average_health_score"] >= 85:

    st.success("""

Overall Field Status

🟢 HEALTHY

The production system is operating normally.

Continue production while monitoring pressure periodically.

""")

elif dashboard["average_health_score"] >= 70:

    st.warning("""

Overall Field Status

🟡 MONITOR

Increase inspection frequency.

""")

elif dashboard["average_health_score"] >= 50:

    st.warning("""

Overall Field Status

🟠 WARNING

Pressure abnormalities detected.

Inspection recommended.

""")

else:

    st.error("""

Overall Field Status

🔴 CRITICAL

Immediate intervention required.

Production risk is high.

""")