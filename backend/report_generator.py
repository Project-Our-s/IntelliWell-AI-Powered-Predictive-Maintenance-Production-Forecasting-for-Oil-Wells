"""
=========================================================
IntelliWell AI Executive Report Generator
=========================================================
Creates a structured executive report from
AI prediction results.
=========================================================
"""

from datetime import datetime


def generate_report(result):
    """
    Generate an executive report
    for a single well prediction.
    """

    report = f"""
=========================================================
                IntelliWell AI Executive Report
=========================================================

Generated On:
{datetime.now().strftime("%d %B %Y %H:%M")}

---------------------------------------------------------
EXECUTIVE SUMMARY
---------------------------------------------------------

{result['AI Summary']}

---------------------------------------------------------
PRODUCTION FORECAST
---------------------------------------------------------

Predicted Production :
{result['Predicted Production']:.2f} Sm³/day

Production Score :
{result['Production Score']:.2f} %

---------------------------------------------------------
PRESSURE ANALYSIS
---------------------------------------------------------

Pressure Status :
{result['Pressure Status']}

Pressure Score :
{result['Pressure Score (%)']:.2f} %

---------------------------------------------------------
WELL HEALTH
---------------------------------------------------------

Well Health Score :
{result['Well Health Score']:.2f} %

Operational Status :
{result['Operational Status']}

---------------------------------------------------------
SMART ALERTS
---------------------------------------------------------

{result['Smart Alerts']}

---------------------------------------------------------
AI ACTION PLAN
---------------------------------------------------------

{result['Action Plan']}

---------------------------------------------------------
FINAL RECOMMENDATION
---------------------------------------------------------

{result['Recommendation']}

---------------------------------------------------------
FORECAST CONFIDENCE
---------------------------------------------------------

Confidence :
{result['Forecast Confidence (%)']:.2f} %

=========================================================
Generated Automatically by IntelliWell AI
=========================================================
"""

    return report