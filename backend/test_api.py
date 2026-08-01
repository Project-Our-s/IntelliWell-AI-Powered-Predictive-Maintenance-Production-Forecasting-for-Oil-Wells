import requests
import json


# ==========================================================
# IntelliWell NLP API Test
# ==========================================================

API_URL = "http://127.0.0.1:5000/analyze-report"

report = """
Possible tubing leakage detected during production.
Pressure loss was observed during operation.
Immediate inspection is recommended.
"""


print("=" * 70)
print("INTELLIWELL NLP API TEST")
print("=" * 70)

print("\nSending report to:")
print(API_URL)

print("\nMaintenance Report:")
print(report)


try:

    response = requests.post(
        API_URL,
        json={
            "report": report
        },
        timeout=30
    )

    print("\nHTTP Status:")
    print(response.status_code)

    print("\n" + "=" * 70)
    print("API RESPONSE")
    print("=" * 70)

    if response.status_code == 200:

        result = response.json()

        print(
            json.dumps(
                result,
                indent=4
            )
        )

        print("\n" + "=" * 70)
        print("INTEGRATION CHECK")
        print("=" * 70)

        print(
            "Category:",
            result.get("category")
        )

        print(
            "Classifier:",
            result.get("classifier")
        )

        print(
            "Confidence:",
            result.get("confidence")
        )

        print(
            "Priority:",
            result.get("priority")
        )

        print(
            "Severity:",
            result.get("severity")
        )

        # ----------------------------------------------
        # Check trained model
        # ----------------------------------------------

        if result.get("classifier") == "Machine Learning":

            print(
                "\n✅ Trained NLP model is being used by Flask."
            )

        else:

            print(
                "\n⚠ Flask is using the rule-based fallback."
            )

    else:

        print(response.text)


except requests.exceptions.ConnectionError:

    print(
        "\n❌ Could not connect to Flask."
    )

    print(
        "Make sure python app.py is running."
    )


except requests.exceptions.Timeout:

    print(
        "\n❌ Flask request timed out."
    )


except Exception as error:

    print(
        "\n❌ Unexpected error:"
    )

    print(error)
