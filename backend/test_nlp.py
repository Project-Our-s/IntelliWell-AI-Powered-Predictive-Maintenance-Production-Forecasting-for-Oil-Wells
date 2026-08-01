from nlp_engine import analyze_report


test_reports = [

    "Downhole pressure dropped significantly after choke adjustment.",

    "Pump vibration increased and abnormal mechanical noise was detected.",

    "Possible tubing leakage detected during production.",

    "Choke valve appears blocked and is not responding correctly.",

    "Electrical sensor reported unstable voltage readings.",

    "Oil production rate declined significantly during operation.",

    "Well is operating normally with stable pressure and temperature."
]


print("=" * 80)
print("INTELLIWELL NLP ENGINE TEST")
print("=" * 80)


for report in test_reports:

    result = analyze_report(report)

    print("\nREPORT:")
    print(report)

    print("\nCATEGORY:")
    print(result["category"])

    print("\nCLASSIFIER:")
    print(result.get("classifier"))

    print("\nCONFIDENCE:")
    print(result.get("confidence"))

    print("\nPRIORITY:")
    print(result["priority"])

    print("\nRECOMMENDATION:")
    print(result["recommendation"])

    print("\n" + "-" * 80)
