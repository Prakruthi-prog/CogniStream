
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "developer_activity_clean.csv"
OUTPUT = ROOT / "reports"

def create_visualizations():
    df = pd.read_csv(INPUT)
    df["date"] = pd.to_datetime(df["date"])
    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Chart 1: Focus ratio trend
    daily = df.groupby("date", as_index=False)[
        "focus_ratio_pct"
    ].mean()

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=daily,
        x="date",
        y="focus_ratio_pct",
        marker="o",
        ax=ax
    )

    ax.set_title(
        "Focus Ratio Trend - Synthetic Sample Data"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Focus Ratio (%)")

    fig.tight_layout()
    fig.savefig(OUTPUT / "focus_trend.png", dpi=150)
    plt.close(fig)

    # Chart 2: Focus ratio by workload
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="self_reported_workload",
        y="focus_ratio_pct",
        ax=ax
    )

    ax.set_title(
        "Focus Ratio by Workload - Sample Data"
    )
    ax.set_xlabel("Self-reported workload (1-5)")
    ax.set_ylabel("Focus Ratio (%)")

    fig.tight_layout()
    fig.savefig(
        OUTPUT / "workload_analysis.png",
        dpi=150
    )
    plt.close(fig)

    print("Visualisations created in the reports folder.")

if __name__ == "__main__":
    create_visualizations()
