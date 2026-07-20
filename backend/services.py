"""
IntelliWell Services

Contains all Machine Learning business logic.
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


# ============================================================
# Production Forecast
# ============================================================

def predict_production(df):

    X = preprocess_production(
        df,
        production_features
    )

    predictions = production_model.predict(X)

    result = df.copy()

    result["Predicted Production"] = predictions

    return result


# ============================================================
# Pressure Anomaly Detection
# ============================================================

def detect_pressure(df):

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

    anomalies = pressure_model.predict(X_scaled)

    scores = pressure_model.decision_function(X_scaled)

    data["Pressure Status"] = anomalies

    data["Pressure Score"] = scores

    return data


# ============================================================
# Well Health Calculation
# ============================================================

def calculate_health(df):

    result = df.copy()

    production_error = abs(

        result["BORE_OIL_VOL"]

        -

        result["Predicted Production"]

    )

    production_score = (

        100 -

        np.clip(
            production_error,
            0,
            100
        )

    )

    pressure_score = (

        (
            result["Pressure Score"]

            -

            result["Pressure Score"].min()

        )

        /

        (

            result["Pressure Score"].max()

            -

            result["Pressure Score"].min()

        )

    ) * 100

    result["Production Score"] = production_score

    result["Pressure Score (%)"] = pressure_score

    result["Well Health Score"] = (

        0.60 * production_score +

        0.40 * pressure_score

    )

    return result


# ============================================================
# Recommendation Engine
# ============================================================

def generate_recommendations(df):

    data = df.copy()

    recommendations = []

    status = []

    for score in data["Well Health Score"]:

        if score >= 85:

            status.append("Healthy")

            recommendations.append(
                "Continue normal production."
            )

        elif score >= 70:

            status.append("Monitor")

            recommendations.append(
                "Increase monitoring frequency."
            )

        elif score >= 50:

            status.append("Warning")

            recommendations.append(
                "Inspect pressure system and choke settings."
            )

        else:

            status.append("Critical")

            recommendations.append(
                "Immediate maintenance required."
            )

    data["Operational Status"] = status

    data["Recommendation"] = recommendations

    return data

# ============================================================
# IntelliWell Complete Pipeline
# ============================================================

def run_pipeline(df):
    """
    Execute the complete IntelliWell workflow.
    """

    result = predict_production(df)

    result = detect_pressure(result)

    result = calculate_health(result)

    result = generate_recommendations(result)

    return result