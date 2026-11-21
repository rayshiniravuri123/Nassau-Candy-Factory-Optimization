
import pandas as pd
import os

print("\n========== NASSAU CANDY PROJECT VALIDATION ==========")

files = [
    "nassau_scenario_distance_analysis.csv",
    "nassau_factory_candidate_comparison.csv",
    "nassau_reallocation_impact_assessment.csv",
    "nassau_factory_scenario_simulation.csv",
    "nassau_best_factory_scenarios.csv",
    "nassau_factory_recommendation_system.csv",
    "nassau_cost_savings_impact_analysis.csv",
    "nassau_business_impact_summary.csv",
    "nassau_factory_business_impact_summary.csv",
    "nassau_final_business_insights.csv"
]

results = []

for filename in files:

    print(f"\nChecking: {filename}")

    if not os.path.exists(filename):
        print("STATUS: FILE NOT FOUND")
        results.append({
            "File": filename,
            "Status": "Missing",
            "Rows": 0,
            "Columns": 0,
            "Missing Values": 0,
            "Duplicate Rows": 0
        })
        continue

    try:
        df = pd.read_csv(filename)

        missing = int(df.isnull().sum().sum())
        duplicates = int(df.duplicated().sum())

        status = "PASS"

        if df.empty:
            status = "FAIL - EMPTY DATASET"

        print("Rows:", len(df))
        print("Columns:", len(df.columns))
        print("Missing values:", missing)
        print("Duplicate rows:", duplicates)
        print("STATUS:", status)

        results.append({
            "File": filename,
            "Status": status,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Values": missing,
            "Duplicate Rows": duplicates
        })

    except Exception as error:

        print("STATUS: READ ERROR")
        print("Error:", error)

        results.append({
            "File": filename,
            "Status": "Read Error",
            "Rows": 0,
            "Columns": 0,
            "Missing Values": 0,
            "Duplicate Rows": 0
        })

report = pd.DataFrame(results)

report.to_csv(
    "nassau_project_validation_report.csv",
    index=False
)

print("\n========== FINAL VALIDATION SUMMARY ==========")
print(report.to_string(index=False))

print("\nValidation report saved successfully.")
