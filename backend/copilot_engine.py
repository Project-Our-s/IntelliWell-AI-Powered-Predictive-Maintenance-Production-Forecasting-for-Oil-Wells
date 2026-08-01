"""
IntelliWell Conversational Maintenance Copilot

Provides contextual answers using the output generated
by the IntelliWell NLP maintenance analysis pipeline.
"""


def generate_copilot_answer(question, analysis):

    question = question.lower().strip()

    category = analysis.get(
        "category",
        "Unknown"
    )

    confidence = analysis.get(
        "confidence"
    )

    priority = analysis.get(
        "priority",
        "Unknown"
    )

    severity = analysis.get(
        "severity",
        0
    )

    root_cause = analysis.get(
        "root_cause",
        "Unknown"
    )

    recommendation = analysis.get(
        "recommendation",
        "No recommendation available."
    )

    actions = analysis.get(
        "actions",
        []
    )

    keywords = analysis.get(
        "keywords",
        []
    )

    summary = analysis.get(
        "summary",
        ""
    )

    # ======================================================
    # Classification explanation
    # ======================================================

    if any(
        phrase in question
        for phrase in [
            "why this classification",
            "why classified",
            "why category",
            "why leak",
            "why pressure",
            "classification"
        ]
    ):

        keyword_text = (
            ", ".join(keywords[:5])
            if keywords
            else "the detected maintenance indicators"
        )

        confidence_text = (
            f"{float(confidence):.2f}%"
            if confidence is not None
            else "not available"
        )

        return (
            f"The report was classified as **{category}** by the "
            f"trained maintenance classifier.\n\n"
            f"Important detected indicators include: "
            f"**{keyword_text}**.\n\n"
            f"The current model confidence indicator is "
            f"**{confidence_text}**."
        )

    # ======================================================
    # Root cause
    # ======================================================

    if any(
        word in question
        for word in [
            "cause",
            "root cause",
            "why happened",
            "reason"
        ]
    ):

        return (
            f"The probable root cause identified by IntelliWell is:\n\n"
            f"**{root_cause}**"
        )

    # ======================================================
    # Severity
    # ======================================================

    if any(
        word in question
        for word in [
            "severity",
            "critical",
            "dangerous",
            "risk"
        ]
    ):

        return (
            f"The current operational severity is "
            f"**{severity}/100**, with a priority of "
            f"**{priority}**.\n\n"
            f"The detected issue category is **{category}**."
        )

    # ======================================================
    # Actions
    # ======================================================

    if any(
        phrase in question
        for phrase in [
            "what should i do",
            "what should we do",
            "action",
            "inspect",
            "first step",
            "next step"
        ]
    ):

        if not actions:

            return (
                "No immediate actions were generated "
                "for this report."
            )

        action_text = "\n".join(
            f"{index}. {action}"
            for index, action in enumerate(
                actions,
                start=1
            )
        )

        return (
            f"For the detected **{category}**, "
            f"IntelliWell recommends:\n\n"
            f"{action_text}\n\n"
            f"Overall recommendation: "
            f"**{recommendation}**"
        )

    # ======================================================
    # Summary
    # ======================================================

    if any(
        word in question
        for word in [
            "summary",
            "summarize",
            "explain report"
        ]
    ):

        return (
            f"**Maintenance Summary**\n\n"
            f"{summary}\n\n"
            f"Classification: **{category}**\n\n"
            f"Priority: **{priority}**"
        )

    # ======================================================
    # Recommendation
    # ======================================================

    if any(
        word in question
        for word in [
            "recommend",
            "recommendation",
            "advice"
        ]
    ):

        return (
            f"IntelliWell recommends:\n\n"
            f"**{recommendation}**"
        )

    # ======================================================
    # Default contextual response
    # ======================================================

    return (
        f"I currently have this report classified as "
        f"**{category}** with **{priority}** priority "
        f"and a severity score of **{severity}/100**.\n\n"
        f"You can ask me about the **classification, root cause, "
        f"severity, recommended actions, keywords, or report summary**."
    )