"""
=========================================================
IntelliWell Services
=========================================================
Contains all Machine Learning business logic.
=========================================================
"""

import numpy as np
import pandas as pd

from preprocess import preprocess_production

from model_loader import (
    production_model,
    production_features,
    pressure_model,
    pressure_scaler,
    pressure_features
)

from ai_engine import (
    generate_ai_summary,
    generate_alerts,
    generate_action_plan
)

from report_generator import generate_report


# ==========================================================
# Production Forecast
# ==========================================================

def predict_production(df):
    """
    Predict oil production using the trained
    Random Forest model.
    """

    X = preprocess_production(
        df,
        production_features
    )

    predictions = production_model.predict(X)

    result = df.copy()

    result["Predicted Production"] = predictions

    return result


# ==========================================================
# Pressure Anomaly Detection
# ==========================================================

def detect_pressure(df):
    """
    Detect pressure anomalies using
    Isolation Forest.
    """

    data = df.copy()

    if "DATEPRD" in data.columns:

        data["DATEPRD"] = pd.to_datetime(data["DATEPRD"])

        data["YEAR"] = data["DATEPRD"].dt.year
        data["MONTH"] = data["DATEPRD"].dt.month
        data["DAY"] = data["DATEPRD"].dt.day
        data["DAY_OF_WEEK"] = data["DATEPRD"].dt.dayofweek

    data.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    X = data[pressure_features].copy()

    X.fillna(
        X.median(numeric_only=True),
        inplace=True
    )

    X_scaled = pressure_scaler.transform(X)

    anomaly_prediction = pressure_model.predict(
        X_scaled
    )

    anomaly_score = pressure_model.decision_function(
        X_scaled
    )

    data["Pressure Prediction"] = anomaly_prediction

    data["Pressure Score"] = anomaly_score

    data["Pressure Status"] = np.where(
        anomaly_prediction == -1,
        "Anomaly",
        "Normal"
    )

    data["Expected Anomaly"] = np.where(
        anomaly_prediction == -1,
        1,
        0
    )

    return data


# ==========================================================
# Well Health Calculation
# ==========================================================

def calculate_health(df):
    """
    Calculate production score,
    pressure score and overall
    health score.
    """

    result = df.copy()

    production_error = abs(

        result["BORE_OIL_VOL"]

        -

        result["Predicted Production"]

    )

    production_score = (

        100

        -

        np.clip(
            production_error,
            0,
            100
        )

    )

    pressure_min = result["Pressure Score"].min()

    pressure_max = result["Pressure Score"].max()

    if pressure_max == pressure_min:

        pressure_score = pd.Series(
            100,
            index=result.index
        )

    else:

        pressure_score = (

            (

                result["Pressure Score"]

                -

                pressure_min

            )

            /

            (

                pressure_max

                -

                pressure_min

            )

        ) * 100

    result["Production Score"] = production_score

    result["Pressure Score (%)"] = pressure_score.round(2)

    result["Well Health Score"] = (

        0.60 * result["Production Score"]

        +

        0.40 * result["Pressure Score (%)"]

    ).round(2)

    return result
# ==========================================================
# Recommendation Engine
# ==========================================================

def generate_recommendations(df):
    """
    Generate operational recommendations
    based on Well Health Score.
    """

    result = df.copy()

    operational_status = []

    recommendations = []

    for score in result["Well Health Score"]:

        if score >= 90:

            operational_status.append(
                "Excellent"
            )

            recommendations.append(
                "Continue normal production."
            )

        elif score >= 75:

            operational_status.append(
                "Healthy"
            )

            recommendations.append(
                "Increase monitoring frequency."
            )

        elif score >= 60:

            operational_status.append(
                "Monitor"
            )

            recommendations.append(
                "Schedule preventive maintenance."
            )

        else:

            operational_status.append(
                "Critical"
            )

            recommendations.append(
                "Immediate maintenance required."
            )

    result["Operational Status"] = operational_status

    result["Recommendation"] = recommendations

    return result


# ==========================================================
# IntelliWell Complete Pipeline
# ==========================================================

def run_pipeline(df):
    """
    Execute the complete IntelliWell workflow.
    """

    # -----------------------------------------
    # Step 1
    # Production Forecast
    # -----------------------------------------

    result = predict_production(df)

    # -----------------------------------------
    # Step 2
    # Pressure Detection
    # -----------------------------------------

    result = detect_pressure(result)

    # -----------------------------------------
    # Step 3
    # Well Health
    # -----------------------------------------

    result = calculate_health(result)
    # Temporary forecast confidence
    result["Forecast Confidence (%)"] = result["Pressure Score (%)"]

    # -----------------------------------------
    # Step 4
    # Recommendations
    # -----------------------------------------

    result = generate_recommendations(result)

    # -----------------------------------------
    # Create Required Columns
    # -----------------------------------------

    result["AI Summary"] = ""

    result["Generated At"] = ""

    result["Smart Alerts"] = ""

    result["Action Plan"] = ""

    result["AI Report"] = ""

    # -----------------------------------------
    # Step 5
    # AI Decision Support
    # -----------------------------------------

    for index, row in result.iterrows():

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

        # -------------------------------------
        # AI Executive Summary
        # -------------------------------------

        ai_result = generate_ai_summary(
            ai_input
        )

        result.at[
            index,
            "AI Summary"
        ] = ai_result["summary"]

        result.at[
            index,
            "Generated At"
        ] = ai_result["generated_at"]

        # -------------------------------------
        # Smart Alerts
        # -------------------------------------

        alerts = generate_alerts(
            ai_input
        )

        result.at[
            index,
            "Smart Alerts"
        ] = "\n".join(alerts)

        # -------------------------------------
        # AI Action Plan
        # -------------------------------------

        action_plan = generate_action_plan(
            ai_input
        )

        result.at[
            index,
            "Action Plan"
        ] = "\n".join(action_plan)

        # -------------------------------------
        # AI Executive Report
        # -------------------------------------

        report_row = result.loc[index].copy()

        report = generate_report(
            report_row
        )

        result.at[
            index,
            "AI Report"
        ] = report
            # -----------------------------------------
    # Final Cleanup
    # -----------------------------------------

    numeric_columns = [
        "Predicted Production",
        "Production Score",
        "Pressure Score",
        "Pressure Score (%)",
        "Well Health Score"
    ]

    for col in numeric_columns:

        if col in result.columns:

            result[col] = result[col].round(2)

    # -----------------------------------------
    # Replace Remaining Missing Values
    # -----------------------------------------

    result.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    result.fillna(
        {
            "AI Summary": "",
            "Smart Alerts": "",
            "Action Plan": "",
            "AI Report": "",
            "Generated At": "",
            "Recommendation": "No recommendation available.",
            "Operational Status": "Unknown"
        },
        inplace=True
    )

    # -----------------------------------------
    # Return Final Result
    # -----------------------------------------

    return result