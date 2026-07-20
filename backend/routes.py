from flask import Blueprint, jsonify, request
import pandas as pd

from services import (
    predict_production,
    detect_pressure,
    run_pipeline
)

api = Blueprint("api", __name__)


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