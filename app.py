
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent

CLEAN_FILE = ROOT / "data" / "developer_activity_clean.csv"
SAMPLE_FILE = ROOT / "data" / "developer_activity_sample.csv"

st.set_page_config(
    page_title="CogniStream Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("CogniStream")
st.subheader("Developer Flow-State & Cognitive Load Analytics")

st.warning(
    "DEMO DASHBOARD: Synthetic sample data only."
)

# Load data
file_path = CLEAN_FILE if CLEAN_FILE.exists() else SAMPLE_FILE
df = pd.read_csv(file_path)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

if "focus_ratio_pct" not in df.columns:
    df["focus_ratio_pct"] = (
        df["focused_minutes"] /
        df["session_minutes"] * 100
    ).round(2)

# Sidebar filters
with st.sidebar:
    st.header("Filters")

    developers = sorted(df["developer_id"].unique())

    selected_developers = st.multiselect(
        "Developer ID",
        developers,
        default=developers
    )

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    selected_dates = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

filtered = df[
    df["developer_id"].isin(selected_developers)
].copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    filtered = filtered[
        (filtered["date"].dt.date >= selected_dates[0]) &
        (filtered["date"].dt.date <= selected_dates[1])
    ]

if filtered.empty:
    st.info("No data found for these filters.")
    st.stop()

# KPI cards
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Focus Ratio",
    f"{filtered['focus_ratio_pct'].mean():.1f}%"
)

c2.metric(
    "Average Interruptions",
    f"{filtered['interruptions'].mean():.1f}"
)

c3.metric(
    "Average Task Switches",
    f"{filtered['task_switches'].mean():.1f}"
)

c4.metric(
    "Average Workload",
    f"{filtered['self_reported_workload'].mean():.1f}/5"
)

# Daily trends
daily = filtered.groupby("date").agg(
    focus_ratio_pct=("focus_ratio_pct", "mean"),
    interruptions=("interruptions", "mean")
)

left, right = st.columns(2)

with left:
    st.subheader("Focus Ratio Trend")
    st.line_chart(daily["focus_ratio_pct"])

with right:
    st.subheader("Average Interruptions")
    st.bar_chart(daily["interruptions"])

# Task switches versus workload
left, right = st.columns(2)

with left:
    st.subheader("Task Switching vs Workload")

    st.scatter_chart(
        filtered,
        x="task_switches",
        y="self_reported_workload",
        color="developer_id"
    )

with right:
    st.subheader("Focus Ratio by Workload")

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.boxplot(
        data=filtered,
        x="self_reported_workload",
        y="focus_ratio_pct",
        ax=ax
    )

    ax.set_xlabel("Self-reported Workload (1-5)")
    ax.set_ylabel("Focus Ratio (%)")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Data table
st.subheader("Developer Activity Records")

st.dataframe(
    filtered.sort_values("date", ascending=False),
    use_container_width=True
)

# CSV download
st.download_button(
    "Download Filtered Data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="cognistream_data.csv",
    mime="text/csv"
)

st.info(
    "These are descriptive workflow indicators, not a "
    "diagnosis or direct measurement of cognitive load."
)
