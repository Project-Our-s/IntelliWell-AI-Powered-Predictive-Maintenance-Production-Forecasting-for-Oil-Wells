import requests
import json


# ==========================================================
# IntelliWell Maintenance Copilot API Test
# ==========================================================

ANALYZE_URL = "http://127.0.0.1:5000/analyze-report"
COPILOT_URL = "http://127.0.0.1:5000/maintenance-copilot"


report = """
Possible tubing leakage detected during production.
Pressure loss was observed during operation.
Immediate inspection is recommended.
"""


print("=" * 70)
print("INTELLIWELL MAINTENANCE COPILOT TEST")
print("=" * 70)


# ==========================================================
# STEP 1 — Analyze Maintenance Report
# ==========================================================

print("\nSTEP 1 — Analyzing maintenance report...\n")

response = requests.post(
    ANALYZE_URL,
    json={
        "report": report
    },
    timeout=30
)


if response.status_code != 200:

    print("❌ Report analysis failed")
    print("Status:", response.status_code)
    print(response.text)

    raise SystemExit


analysis = response.json()


print("✅ Report analyzed successfully")

print("\nCategory:")
print(analysis.get("category"))

print("\nClassifier:")
print(analysis.get("classifier"))

print("\nPriority:")
print(analysis.get("priority"))

print("\nSeverity:")
print(analysis.get("severity"))


# ==========================================================
# STEP 2 — Test Copilot Questions
# ==========================================================

questions = [

    "Why was this classified as a leak?",

    "What is the probable root cause?",

    "Why is this critical?",

    "What should I inspect first?",

    "Summarize the report.",

    "What do you recommend?"
]


print("\n" + "=" * 70)
print("STEP 2 — COPILOT CONVERSATION")
print("=" * 70)


for question in questions:

    print("\n🧑 ENGINEER:")
    print(question)

    copilot_response = requests.post(
        COPILOT_URL,
        json={
            "question": question,
            "analysis": analysis
        },
        timeout=30
    )


    if copilot_response.status_code == 200:

        data = copilot_response.json()

        print("\n🤖 INTELLIWELL:")

        print(
            data.get(
                "answer",
                "No answer returned."
            )
        )

    else:

        print("\n❌ COPILOT ERROR")

        print(
            "HTTP Status:",
            copilot_response.status_code
        )

        print(
            copilot_response.text
        )

    print("\n" + "-" * 70)


print("\n✅ Copilot API test completed.")