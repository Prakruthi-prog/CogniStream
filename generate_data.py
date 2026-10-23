
import pandas as pd
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "developer_activity_sample.csv"

def generate_data():
    random.seed(42)
    rows = []

    for i in range(120):
        session = random.randint(35, 180)

        rows.append({
            "date": (
                date(2026, 9, 1) +
                timedelta(days=i % 30)
            ).isoformat(),
            "developer_id": f"DEV{(i % 12) + 1:02d}",
            "session_minutes": session,
            "focused_minutes": random.randint(15, session),
            "interruptions": random.randint(0, 10),
            "task_switches": random.randint(0, 16),
            "self_reported_workload": random.randint(1, 5),
            "tasks_completed": random.randint(0, 9)
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTPUT, index=False)

    print("Sample dataset generated successfully!")
    print("Total records:", len(rows))
    print("Saved at:", OUTPUT)

if __name__ == "__main__":
    generate_data()
