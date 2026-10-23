
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "developer_activity_clean.csv"
REPORTS = ROOT / "reports"

def analyze_data():
    df = pd.read_csv(INPUT)
    REPORTS.mkdir(parents=True, exist_ok=True)

    metrics = {
        "Total sessions": len(df),
        "Unique developers": df["developer_id"].nunique(),
        "Average focus ratio (%)": round(
            df["focus_ratio_pct"].mean(), 2
        ),
        "Average interruptions": round(
            df["interruptions"].mean(), 2
        ),
        "Average task switches": round(
            df["task_switches"].mean(), 2
        ),
        "Average workload": round(
            df["self_reported_workload"].mean(), 2
        ),
        "Total tasks completed": int(
            df["tasks_completed"].sum()
        )
    }

    summary = pd.DataFrame(
        list(metrics.items()),
        columns=["Metric", "Value"]
    )

    summary.to_csv(
        REPORTS / "summary.csv",
        index=False
    )

    print("\nCOGNISTREAM ANALYTICS SUMMARY")
    print(summary.to_string(index=False))

    corr = df["task_switches"].corr(
        df["self_reported_workload"]
    )

    report = f"""# CogniStream Analysis Report

**Dataset:** Synthetic sample data.

## Key findings

- Total sessions: {len(df)}
- Average focus ratio: {df['focus_ratio_pct'].mean():.2f}%
- Average interruptions: {df['interruptions'].mean():.2f}
- Average task switches: {df['task_switches'].mean():.2f}
- Average workload: {df['self_reported_workload'].mean():.2f}/5
- Total tasks completed: {int(df['tasks_completed'].sum())}
- Correlation between task switching and workload: {corr:.2f}

## Limitations

These results use simulated data. Correlation does not
prove causation. The metrics are workflow indicators and
cannot directly diagnose cognitive load or establish flow state.
"""

    (REPORTS / "insights_report.md").write_text(
        report, encoding="utf-8"
    )

    print("\nSummary and insights report generated.")

if __name__ == "__main__":
    analyze_data()
