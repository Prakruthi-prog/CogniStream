
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "developer_activity_sample.csv"
OUTPUT = ROOT / "data" / "developer_activity_clean.csv"

def clean_data():
    df = pd.read_csv(INPUT)

    required = [
        "date", "developer_id",
        "session_minutes", "focused_minutes",
        "interruptions", "task_switches",
        "self_reported_workload", "tasks_completed"
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df[required].copy()

    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )

    numeric_columns = [
        "session_minutes", "focused_minutes",
        "interruptions", "task_switches",
        "self_reported_workload", "tasks_completed"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before = len(df)

    df = df.dropna(subset=required)
    df = df.drop_duplicates()

    df = df[
        (df["session_minutes"] > 0) &
        (df["focused_minutes"] >= 0) &
        (df["focused_minutes"] <= df["session_minutes"]) &
        (df["interruptions"] >= 0) &
        (df["task_switches"] >= 0) &
        (df["self_reported_workload"].between(1, 5)) &
        (df["tasks_completed"] >= 0)
    ].copy()

    df["focus_ratio_pct"] = (
        df["focused_minutes"] /
        df["session_minutes"] * 100
    ).round(2)

    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    df.to_csv(OUTPUT, index=False)

    print("Data cleaning completed!")
    print("Rows before cleaning:", before)
    print("Rows after cleaning:", len(df))
    print("Output:", OUTPUT)

if __name__ == "__main__":
    clean_data()
