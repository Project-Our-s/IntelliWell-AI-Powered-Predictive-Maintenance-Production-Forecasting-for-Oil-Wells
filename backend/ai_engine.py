"""
===========================================
IntelliWell AI Engine
Phase 1
AI Summary Generator
===========================================
"""

from datetime import datetime


def generate_ai_summary(result):
    """
    Generate an executive summary
    from ML predictions.
    """

    production = result["Predicted Production"]

    health = result["Well Health Score"]

    pressure = result["Pressure Status"]

    anomaly = result["Expected Anomaly"]

    recommendation = result["Recommendation"]

    confidence = result["Forecast Confidence (%)"]

    summary = []

    summary.append(
        f"Predicted production is "
        f"{production:.2f} Sm³/day."
    )

    summary.append(
        f"Overall well health score "
        f"is {health:.1f}%."
    )

    summary.append(
        f"Pressure condition is "
        f"{pressure.lower()}."
    )

    if anomaly == 0:

        summary.append(
            "No pressure anomalies "
            "are expected."
        )

    else:

        summary.append(
            f"{anomaly} pressure anomaly"
            f"{' is' if anomaly==1 else 'ies are'} "
            "expected."
        )

    summary.append(
        f"Forecast confidence is "
        f"{confidence:.1f}%."
    )

    summary.append(
        f"AI Recommendation: "
        f"{recommendation}."
    )

    return {

        "generated_at":

            datetime.now().strftime(
                "%d %B %Y %H:%M"
            ),

        "summary":

            " ".join(summary)

    }
# ============================================
# Smart Alert Engine
# ============================================

def generate_alerts(result):
    """
    Generate intelligent operational alerts.
    """

    alerts = []

    health = result["Well Health Score"]

    pressure = result["Pressure Status"]

    anomaly = result["Expected Anomaly"]

    production = result["Predicted Production"]

    confidence = result["Forecast Confidence (%)"]

    # ----------------------------------------
    # Health Alerts
    # ----------------------------------------

    if health < 50:

        alerts.append(
            "🔴 Critical: Well health is below 50%. Immediate maintenance required."
        )

    elif health < 70:

        alerts.append(
            "🟠 Warning: Well health is declining. Increase monitoring."
        )

    elif health < 85:

        alerts.append(
            "🟡 Monitor: Well health is stable but requires observation."
        )

    else:

        alerts.append(
            "🟢 Well health is excellent."
        )

    # ----------------------------------------
    # Pressure Alerts
    # ----------------------------------------

    if pressure == "Anomaly":

        alerts.append(
            "⚠ Pressure anomaly detected."
        )

    else:

        alerts.append(
            "✅ Pressure remains stable."
        )

    # ----------------------------------------
    # Expected Anomaly
    # ----------------------------------------

    if anomaly > 0:

        alerts.append(
            f"⚠ {anomaly} expected pressure anomaly detected."
        )

    # ----------------------------------------
    # Confidence
    # ----------------------------------------

    if confidence < 70:

        alerts.append(
            "⚠ Forecast confidence is relatively low."
        )

    # ----------------------------------------
    # Production
    # ----------------------------------------

    if production < 500:

        alerts.append(
            "📉 Production is relatively low."
        )

    return alerts
# ============================================
# AI Decision Engine
# ============================================

def generate_action_plan(result):
    """
    Generate an intelligent maintenance
    and operational action plan.
    """

    plan = []

    health = result["Well Health Score"]

    pressure = result["Pressure Status"]

    anomaly = result["Expected Anomaly"]

    production = result["Predicted Production"]

    confidence = result["Forecast Confidence (%)"]

    # ------------------------------------
    # Health Based Actions
    # ------------------------------------

    if health >= 90:

        plan.append(
            "Continue normal production."
        )

        plan.append(
            "Maintain routine inspection schedule."
        )

    elif health >= 75:

        plan.append(
            "Increase monitoring frequency."
        )

        plan.append(
            "Inspect pressure trends during the next production cycle."
        )

    elif health >= 60:

        plan.append(
            "Schedule preventive maintenance."
        )

        plan.append(
            "Inspect tubing and choke valve."
        )

        plan.append(
            "Review pressure history."
        )

    else:

        plan.append(
            "Immediate maintenance required."
        )

        plan.append(
            "Reduce production until inspection is completed."
        )

        plan.append(
            "Inspect pump, tubing and pressure sensors."
        )

    # ------------------------------------
    # Pressure Actions
    # ------------------------------------

    if pressure == "Anomaly":

        plan.append(
            "Pressure anomaly detected. Verify sensor readings."
        )

        plan.append(
            "Inspect annulus and downhole pressure."
        )

    # ------------------------------------
    # Production Actions
    # ------------------------------------

    if production < 500:

        plan.append(
            "Production below expected level."
        )

        plan.append(
            "Evaluate production optimization strategies."
        )

    # ------------------------------------
    # Confidence
    # ------------------------------------

    if confidence < 70:

        plan.append(
            "Forecast confidence is low."
        )

        plan.append(
            "Collect additional operational data."
        )

    # ------------------------------------
    # Future Risk
    # ------------------------------------

    if anomaly > 0:

        plan.append(
            "Increase inspection frequency over the forecast horizon."
        )

    return plan