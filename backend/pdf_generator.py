"""
=========================================================
IntelliWell AI PDF Report Generator
=========================================================
Converts AI Executive Report into a professional PDF.
=========================================================
"""

import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def create_pdf_report(result, output_path="IntelliWell_Report.pdf"):
    """
    Create a professional PDF report for one well.

    Parameters
    ----------
    result : pandas.Series or dict
        One prediction row.

    output_path : str
        PDF file name.

    Returns
    -------
    str
        Path of generated PDF.
    """

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    doc = SimpleDocTemplate(
        output_path,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    elements = []

    # ====================================================
    # Title
    # ====================================================

    elements.append(
        Paragraph(
            "🤖 IntelliWell AI Executive Report",
            title_style
        )
    )

    elements.append(Spacer(1, 0.30 * inch))

    elements.append(
        Paragraph(
            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%d %B %Y %H:%M')}",
            body_style
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    # ====================================================
    # Well Information
    # ====================================================

    elements.append(
        Paragraph(
            "Well Information",
            heading_style
        )
    )

    info = [

        ["Well",
         result.get("NPD_WELL_BORE_NAME", "N/A")],

        ["Field",
         result.get("NPD_FIELD_NAME", "N/A")],

        ["Facility",
         result.get("NPD_FACILITY_NAME", "N/A")],

        ["Forecast Date",
         str(result.get("Forecast Date", "N/A"))],

        ["Forecast Days",
         str(result.get("Forecast Days", "N/A"))]

    ]

    table = Table(info, colWidths=[2 * inch, 4 * inch])

    table.setStyle(

        TableStyle(

            [

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ]

        )

    )

    elements.append(table)

    elements.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # Executive Summary
    # ====================================================

    elements.append(
        Paragraph(
            "AI Executive Summary",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            result.get("AI Summary", "No summary available."),
            body_style
        )
    )

    elements.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # Prediction Results
    # ====================================================

    elements.append(
        Paragraph(
            "Prediction Results",
            heading_style
        )
    )

    prediction = [

        ["Predicted Production",
         f"{result.get('Predicted Production',0):.2f} Sm³/day"],

        ["Production Score",
         f"{result.get('Production Score',0):.2f}%"],

        ["Pressure Status",
         str(result.get("Pressure Status","N/A"))],

        ["Pressure Score",
         f"{result.get('Pressure Score (%)',0):.2f}%"],

        ["Health Score",
         f"{result.get('Well Health Score',0):.2f}%"],

        ["Operational Status",
         result.get("Operational Status","N/A")],

        ["Forecast Confidence",
         f"{result.get('Forecast Confidence (%)',0):.2f}%"]

    ]

    table = Table(prediction, colWidths=[2.5 * inch, 3.5 * inch])

    table.setStyle(

        TableStyle(

            [

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ]

        )

    )

    elements.append(table)

    elements.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # Smart Alerts
    # ====================================================

    elements.append(
        Paragraph(
            "Smart Alerts",
            heading_style
        )
    )

    alerts = result.get("Smart Alerts", "")

    for alert in alerts.split("\n"):

        elements.append(
            Paragraph(f"• {alert}", body_style)
        )

    elements.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # Action Plan
    # ====================================================

    elements.append(
        Paragraph(
            "AI Action Plan",
            heading_style
        )
    )

    actions = result.get("Action Plan", "")

    for action in actions.split("\n"):

        elements.append(
            Paragraph(f"• {action}", body_style)
        )

    elements.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # Recommendation
    # ====================================================

    elements.append(
        Paragraph(
            "Final Recommendation",
            heading_style
        )
    )

    elements.append(

        Paragraph(

            result.get("Recommendation", "N/A"),

            body_style

        )

    )

    elements.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # Footer
    # ====================================================

    elements.append(
        Paragraph(
            "<b>Generated automatically by IntelliWell AI Decision Support System</b>",
            body_style
        )
    )

    doc.build(elements)

    return os.path.abspath(output_path)