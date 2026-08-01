import streamlit as st
import requests

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="IntelliWell AI Maintenance Copilot",
    page_icon="🧠",
    layout="wide"
)

API_URL = "http://127.0.0.1:5000/analyze-report"
COPILOT_URL = "http://127.0.0.1:5000/maintenance-copilot"

if "maintenance_analysis" not in st.session_state:
    st.session_state["maintenance_analysis"] = None

if "copilot_messages" not in st.session_state:
    st.session_state["copilot_messages"] = []

# ==========================================================
# Copilot Session State
# ==========================================================

if "copilot_messages" not in st.session_state:
    st.session_state.copilot_messages = []

if "maintenance_analysis" not in st.session_state:
    st.session_state.maintenance_analysis = None

if "maintenance_report" not in st.session_state:
    st.session_state.maintenance_report = None


# ==========================================================
# Header
# ==========================================================

st.title("🧠 IntelliWell AI Maintenance Copilot")

st.markdown(
    """
    Analyze petroleum well maintenance reports using IntelliWell's
    Natural Language Processing and decision-support engine.
    """
)

st.divider()


# ==========================================================
# Maintenance Report Input
# ==========================================================

st.subheader("📝 Maintenance Report")

report = st.text_area(
    "Enter or paste an engineer's maintenance report",
    height=220,
    placeholder=(
        "Example:\n\n"
        "Pressure dropped significantly after choke adjustment. "
        "Pump vibration increased during production. "
        "Possible tubing leak detected. "
        "Inspection recommended immediately."
    )
)


# ==========================================================
# Analyze Button
# ==========================================================

analyze_button = st.button(
    "🤖 Analyze Maintenance Report",
    type="primary",
    use_container_width=True
)


# ==========================================================
# NLP Analysis
# ==========================================================

if analyze_button:

    if not report.strip():

        st.warning(
            "Please enter a maintenance report before running the analysis."
        )

        st.stop()

    try:

        with st.spinner(
            "IntelliWell NLP Engine is analyzing the report..."
        ):

            response = requests.post(
                API_URL,
                json={
                    "report": report
                },
                timeout=30
            )

        # ----------------------------------------------
        # Check API response
        # ----------------------------------------------

        if response.status_code != 200:

            try:
                error_data = response.json()
                error_message = error_data.get(
                    "error",
                    "Unknown backend error."
                )

            except Exception:
                error_message = response.text

            st.error(
                f"Backend returned an error: {error_message}"
            )

            st.stop()

        result = response.json()
        st.session_state["maintenance_analysis"] = result
        # Save analysis for IntelliWell Copilot
        st.session_state["maintenance_analysis"] = result

        # Reset chat only when a NEW report is analyzed
        st.session_state["copilot_messages"] = []

        st.success(
            "Maintenance report analyzed successfully."
        )

        st.divider()


        # ==================================================
        # KPI Section
        # ==================================================

        st.subheader("📊 Maintenance Intelligence")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Issue Category",
            result.get(
                "category",
                "Unknown"
            )
        )

        col2.metric(
            "Priority",
            result.get(
                "priority",
                "Unknown"
            )
        )

        col3.metric(
            "Severity Score",
            f"{result.get('severity', 0)}/100"
        )

        confidence = result.get(
        "confidence"
            )

        if confidence is None:
             confidence_display = "N/A"
        else:
         confidence_display = f"{float(confidence):.2f}%"

        col4.metric(
        "Model Confidence",
        confidence_display
            )


        # ==================================================
        # Severity Indicator
        # ==================================================

        severity = result.get(
            "severity",
            0
        )

        st.markdown("### ⚠️ Operational Severity")

        st.progress(
            min(
                max(
                    int(severity),
                    0
                ),
                100
            )
        )

        if severity >= 90:

            st.error(
                "Critical operational condition detected."
            )

        elif severity >= 70:

            st.warning(
                "High operational risk detected."
            )

        elif severity >= 40:

            st.info(
                "Moderate operational attention recommended."
            )

        else:

            st.success(
                "Low operational risk."
            )

        st.divider()


        # ==================================================
        # AI Summary
        # ==================================================

        st.subheader("🤖 AI Summary")

        st.info(
            result.get(
                "summary",
                "No summary available."
            )
        )


        # ==================================================
        # Root Cause
        # ==================================================

        st.subheader("🔍 Probable Root Cause")

        st.warning(
            result.get(
                "root_cause",
                "Root cause could not be determined."
            )
        )


        # ==================================================
        # Immediate Actions
        # ==================================================

        st.subheader("🛠 Recommended Immediate Actions")

        actions = result.get(
            "actions",
            []
        )

        if actions:

            for number, action in enumerate(
                actions,
                start=1
            ):

                st.markdown(
                    f"**{number}.** {action}"
                )

        else:

            st.write(
                "No immediate actions generated."
            )


        # ==================================================
        # Recommendation
        # ==================================================

        st.subheader("💡 IntelliWell Recommendation")

        st.success(
            result.get(
                "recommendation",
                "No recommendation available."
            )
        )


        # ==================================================
        # Keywords
        # ==================================================

        st.subheader("🔑 Detected Keywords")

        keywords = result.get(
            "keywords",
            []
        )

        if keywords:

            keyword_columns = st.columns(
                min(
                    len(keywords),
                    5
                )
            )

            for index, keyword in enumerate(
                keywords
            ):

                column = keyword_columns[
                    index % len(keyword_columns)
                ]

                column.code(
                    keyword
                )

        else:

            st.write(
                "No significant keywords detected."
            )


        # ==================================================
        # Additional NLP Information
        # ==================================================

        st.subheader("📑 NLP Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown("#### Sentiment")

            st.write(
                result.get(
                    "sentiment",
                    "Unknown"
                )
            )

        with col2:

            st.markdown("#### Classification")

            st.write(
                result.get(
                    "category",
                    "Unknown"
                )
            )

        with col3:

            st.markdown("#### Classifier")

            st.write(
                result.get(
                    "classifier",
                    "Unknown"
                )
            )        
        # ==================================================
        # Cleaned NLP Text
        # ==================================================

        with st.expander(
            "🧹 View NLP Preprocessed Text"
        ):

            st.code(
                result.get(
                    "clean_report",
                    ""
                )
            )


        # ==================================================
        # Original Report
        # ==================================================

        with st.expander(
            "📄 View Original Maintenance Report"
        ):

            st.write(
                result.get(
                    "original_report",
                    report
                )
            )


        # ==================================================
        # Developer View
        # ==================================================

        with st.expander(
            "⚙️ Developer View — API Response"
        ):

            st.json(
                result
            )


    # ======================================================
    # Backend Connection Error
    # ======================================================

    except requests.exceptions.ConnectionError:

        st.error(
            """
            Cannot connect to the IntelliWell Flask backend.

            Start the backend using:

            python app.py
            """
        )


    # ======================================================
    # Timeout
    # ======================================================

    except requests.exceptions.Timeout:

        st.error(
            "The NLP API took too long to respond."
        )


    # ======================================================
    # Other Errors
    # ======================================================

    except Exception as error:

        st.error(
            f"Unexpected error: {error}"
        )
        # ==================================================
        # Classification Engine
        # ==================================================

        classifier = result.get(
            "classifier",
            "Unknown"
        )

        if classifier == "Machine Learning":

            st.success(
                "🤖 Classification Engine: Trained Machine Learning Model"
            )

        elif classifier == "Rule-Based Fallback":

            st.warning(
                "⚠️ Classification Engine: Rule-Based Fallback"
            )

        else:

            st.info(
                f"Classification Engine: {classifier}"
            )


        # ==================================================
        # Model Confidence Indicator
        # ==================================================

        confidence = result.get(
            "confidence"
        )

        if confidence is not None:

            confidence_value = float(
                confidence
            )

            st.markdown(
                "### 🎯 Classification Confidence"
            )

            st.progress(
                min(
                    max(
                        int(confidence_value),
                        0
                    ),
                    100
                )
            )

            if confidence_value >= 85:

                st.success(
                    "High model confidence."
                )

            elif confidence_value >= 70:

                st.info(
                    "Moderate model confidence."
                )

            else:

                st.warning(
                    "Lower model confidence — engineering review recommended."
                )
# ==========================================================
# IntelliWell Conversational Copilot
# ==========================================================

st.divider()
st.subheader("💬 Ask IntelliWell")

if "copilot_messages" not in st.session_state:
    st.session_state["copilot_messages"] = []

analysis = st.session_state.get("maintenance_analysis", None)

if analysis:

    st.success("🟢 IntelliWell Copilot Active")

    # Display previous conversation
    for message in st.session_state["copilot_messages"]:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Actual prompt input
    prompt = st.chat_input(
        "Ask IntelliWell a question about this report..."
    )

    if prompt:

        st.session_state["copilot_messages"].append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        try:

            copilot_response = requests.post(
                "http://127.0.0.1:5000/maintenance-copilot",
                json={
                    "question": prompt,
                    "analysis": analysis
                },
                timeout=30
            )

            if copilot_response.status_code == 200:

                answer = copilot_response.json().get(
                    "answer",
                    "No answer generated."
                )

            else:

                answer = (
                    f"Copilot API returned "
                    f"HTTP {copilot_response.status_code}."
                )

        except requests.exceptions.ConnectionError:

            answer = (
                "Cannot connect to the IntelliWell backend."
            )

        except Exception as error:

            answer = f"Copilot error: {error}"

        st.session_state["copilot_messages"].append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.markdown(answer)

else:

    st.warning(
        "Copilot is waiting for a maintenance analysis. "
        "Enter a report above and click Analyze Maintenance Report."
    )