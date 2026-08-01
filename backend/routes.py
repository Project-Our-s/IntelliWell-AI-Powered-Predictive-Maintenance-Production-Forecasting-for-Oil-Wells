from flask import Blueprint, jsonify, request
import pandas as pd
from nlp_engine import analyze_report
from copilot_engine import generate_copilot_answer
from services import (
    predict_production,
    detect_pressure,
    run_pipeline
)
from flask import Blueprint, request, jsonify

import streamlit as st
import requests


api = Blueprint("api", __name__)

# ==========================================================
# IntelliWell Copilot Session State
# ==========================================================

if "maintenance_analysis" not in st.session_state:
    st.session_state.maintenance_analysis = None

if "copilot_messages" not in st.session_state:
    st.session_state.copilot_messages = []
# ==========================================================
# Health Check
# ==========================================================

@api.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "API Running Successfully"
    })


# ==========================================================
# Helper Function
# ==========================================================

def load_uploaded_file(file):
    """
    Load uploaded CSV or Excel file.
    """

    if file.filename.endswith(".xlsx"):
        return pd.read_excel(file)

    elif file.filename.endswith(".csv"):
        return pd.read_csv(file)

    else:
        raise ValueError(
            "Only CSV and Excel files are supported."
        )


# ==========================================================
# Production Forecast
# ==========================================================

@api.route("/predict-production", methods=["POST"])
def production_prediction():

    try:

        if "file" not in request.files:

            return jsonify({
                "status": "error",
                "message": "No file uploaded."
            }), 400

        df = load_uploaded_file(request.files["file"])

        result = predict_production(df)

        response = {

            "status": "success",

            "records_processed": len(result),

            "average_prediction": float(
                result["Predicted Production"].mean()
            ),

            "maximum_prediction": float(
                result["Predicted Production"].max()
            ),

            "minimum_prediction": float(
                result["Predicted Production"].min()
            ),

            "predictions": result[
                ["Predicted Production"]
            ].head(20).to_dict(
                orient="records"
            )

        }

        return jsonify(response)

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==========================================================
# Pressure Anomaly Detection
# ==========================================================

@api.route("/detect-pressure", methods=["POST"])
def pressure_detection():

    try:

        if "file" not in request.files:

            return jsonify({

                "status": "error",

                "message": "No file uploaded."

            }), 400

        df = load_uploaded_file(request.files["file"])

        result = detect_pressure(df)

        anomaly_count = int(
            (result["Pressure Status"] == -1).sum()
        )

        response = {

            "status": "success",

            "records_processed": len(result),

            "pressure_anomalies": anomaly_count,

            "average_pressure_score": float(
                result["Pressure Score"].mean()
            ),

            "maximum_pressure_score": float(
                result["Pressure Score"].max()
            ),

            "minimum_pressure_score": float(
                result["Pressure Score"].min()
            )

        }

        return jsonify(response)

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==========================================================
# Well Health Assessment
# ==========================================================

@api.route("/well-health", methods=["POST"])
def well_health():

    try:

        if "file" not in request.files:

            return jsonify({

                "status": "error",

                "message": "No file uploaded."

            }), 400

        df = load_uploaded_file(request.files["file"])

        result = run_pipeline(df)

        response = {

            "status": "success",

            "records_processed": len(result),

            "average_health_score": float(
                result["Well Health Score"].mean()
            ),

            "maximum_health_score": float(
                result["Well Health Score"].max()
            ),

            "minimum_health_score": float(
                result["Well Health Score"].min()
            )

        }

        return jsonify(response)

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==========================================================
# Recommendation Engine
# ==========================================================

@api.route("/recommendation", methods=["POST"])
def recommendation():

    try:

        if "file" not in request.files:

            return jsonify({

                "status": "error",

                "message": "No file uploaded."

            }), 400

        df = load_uploaded_file(request.files["file"])

        result = run_pipeline(df)

        recommendations = result[
            [
                "Operational Status",
                "Recommendation"
            ]
        ].head(20)

        return jsonify({

            "status": "success",

            "recommendations": recommendations.to_dict(
                orient="records"
            )

        })

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


# ==========================================================
# Executive Dashboard
# ==========================================================

@api.route("/dashboard-summary", methods=["POST"])
def dashboard_summary():

    try:

        if "file" not in request.files:

            return jsonify({

                "status": "error",

                "message": "No file uploaded."

            }), 400

        df = load_uploaded_file(request.files["file"])

        result = run_pipeline(df)

        dashboard = {

            "status": "success",

            "records_processed": len(result),

            "average_predicted_production": float(
                result["Predicted Production"].mean()
            ),

            "average_health_score": float(
                result["Well Health Score"].mean()
            ),

            "pressure_anomalies": int(
                (result["Pressure Status"] == -1).sum()
            ),

            "healthy": int(
                (result["Operational Status"] == "Healthy").sum()
            ),

            "monitor": int(
                (result["Operational Status"] == "Monitor").sum()
            ),

            "warning": int(
                (result["Operational Status"] == "Warning").sum()
            ),

            "critical": int(
                (result["Operational Status"] == "Critical").sum()
            )

        }

        return jsonify(dashboard)

    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500

# ==========================================================
# NLP Maintenance Report Analysis
# ==========================================================

@api.route("/analyze-report", methods=["POST"])
def analyze_maintenance_report():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "No JSON received."
            }), 400

        report = data.get("report", "").strip()

        if not report:

            return jsonify({
                "error": "Maintenance report is empty."
            }), 400

        result = analyze_report(report)

        return jsonify(result)
        st.session_state.maintenance_analysis = result
        st.session_state.copilot_messages = []
    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@api.route(
    "/maintenance-copilot",
    methods=["POST"]
)

# ==========================================================
# IntelliWell Maintenance Copilot
# ==========================================================

@api.route(
    "/maintenance-copilot",
    methods=["POST"]
)
def maintenance_copilot():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required."
            }), 400

        question = data.get(
            "question",
            ""
        ).strip()

        analysis = data.get(
            "analysis"
        )

        if not question:
            return jsonify({
                "error": "Question is required."
            }), 400

        if not analysis:
            return jsonify({
                "error": "Maintenance analysis is required."
            }), 400

        answer = generate_copilot_answer(
            question,
            analysis
        )

        return jsonify({
            "answer": answer
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500
# ==========================================================
# IntelliWell Conversational Copilot
# ==========================================================

st.divider()

st.subheader("💬 Ask IntelliWell")

analysis = st.session_state.get(
    "maintenance_analysis"
)

if analysis is None:

    st.info(
        "Analyze a maintenance report first to activate IntelliWell Copilot."
    )

else:

    st.caption(
        "Ask IntelliWell questions about the analyzed maintenance report."
    )

    # ------------------------------------------------------
    # Display conversation history
    # ------------------------------------------------------

    for message in st.session_state.copilot_messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    # ------------------------------------------------------
    # Chat input
    # ------------------------------------------------------

    user_question = st.chat_input(
        "Ask IntelliWell about this maintenance report..."
    )

    # ------------------------------------------------------
    # Process question
    # ------------------------------------------------------

    if user_question:

        # Save user message
        st.session_state.copilot_messages.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):

            st.markdown(
                user_question
            )

        try:

            # ----------------------------------------------
            # Call Flask Copilot API
            # ----------------------------------------------

            copilot_response = requests.post(
                "http://127.0.0.1:5000/maintenance-copilot",
                json={
                    "question": user_question,
                    "analysis": analysis
                },
                timeout=30
            )

            # ----------------------------------------------
            # Successful response
            # ----------------------------------------------

            if copilot_response.status_code == 200:

                data = copilot_response.json()

                answer = data.get(
                    "answer",
                    "No response was generated."
                )

            else:

                answer = (
                    "IntelliWell could not answer the question. "
                    f"API status: {copilot_response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            answer = (
                "The IntelliWell backend is unavailable. "
                "Make sure Flask is running."
            )

        except requests.exceptions.Timeout:

            answer = (
                "The IntelliWell Copilot request timed out."
            )

        except Exception as error:

            answer = (
                f"An unexpected Copilot error occurred: {error}"
            )

        # ----------------------------------------------
        # Save assistant response
        # ----------------------------------------------

        st.session_state.copilot_messages.append({
            "role": "assistant",
            "content": answer
        })

        # ----------------------------------------------
        # Display assistant response
        # ----------------------------------------------

        with st.chat_message("assistant"):

            st.markdown(
                answer
            )