"""Synthetic poll generation, validation, analysis, charts, and insights."""
from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Supports headless runs and CI environments.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OPTIONS = ["Option A", "Option B", "Option C", "Option D"]
REGIONS = ["North", "South", "East", "West"]
AGE_GROUPS = ["18-24", "25-34", "35-44", "45+"]
QUESTION = "Which product feature matters most to you?"
REQUIRED_COLUMNS = ["respondent_id", "response_date", "question", "selected_option", "region", "age_group"]
COLORS = ["#276EF1", "#16A085", "#F39C12", "#8E44AD"]


def generate_synthetic_data(n: int = 600, seed: int = 42) -> pd.DataFrame:
    """Create a fictional, reproducible one-question poll with mild segment effects."""
    if n < 20:
        raise ValueError("Please generate at least 20 responses for useful comparisons.")
    rng = np.random.default_rng(seed)
    regions = rng.choice(REGIONS, n, p=[.28, .27, .20, .25])
    ages = rng.choice(AGE_GROUPS, n, p=[.24, .34, .23, .19])
    dates = pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 90, n), unit="D")
    base = np.array([.34, .29, .23, .14])
    region_effect = {"North": [0, .04, -.02, -.02], "South": [-.03, .02, .02, -.01],
                     "East": [.02, -.03, .01, 0], "West": [.01, -.02, -.01, .02]}
    age_effect = {"18-24": [-.04, .04, .02, -.02], "25-34": [.01, .01, -.01, -.01],
                  "35-44": [.03, -.01, 0, -.02], "45+": [.02, -.03, -.01, .02]}
    selected = []
    for region, age in zip(regions, ages):
        weights = np.clip(base + region_effect[region] + age_effect[age], .04, None)
        weights = weights / weights.sum()
        selected.append(rng.choice(OPTIONS, p=weights))
    frame = pd.DataFrame({
        "respondent_id": [f"R{i:05d}" for i in range(1, n + 1)],
        "response_date": dates,
        "question": QUESTION,
        "selected_option": selected,
        "region": regions,
        "age_group": ages,
    })
    # Add a few realistic quality issues so cleaning is visible and demonstrable.
    if n >= 100:
        frame.loc[frame.index[::137], "region"] = "  " + frame.loc[frame.index[::137], "region"] + "  "
        frame.loc[frame.index[::211], "selected_option"] = frame.loc[frame.index[::211], "selected_option"].str.lower()
    return frame


def clean_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Normalize fields and drop unusable rows/duplicate respondent-question pairs."""
    missing = sorted(set(REQUIRED_COLUMNS) - set(raw.columns))
    if missing:
        raise ValueError(f"Input CSV is missing required columns: {', '.join(missing)}")
    data = raw[REQUIRED_COLUMNS].copy()
    original_rows = len(data)
    for column in ["respondent_id", "question", "selected_option", "region", "age_group"]:
        data[column] = data[column].astype("string").str.strip()
    data["selected_option"] = data["selected_option"].str.upper().replace({o.upper(): o for o in OPTIONS})
    data["response_date"] = pd.to_datetime(data["response_date"], errors="coerce")
    data = data.dropna(subset=REQUIRED_COLUMNS)
    data = data[data["respondent_id"].ne("") & data["question"].ne("")]
    data = data[data["selected_option"].isin(OPTIONS)]
    data = data.drop_duplicates(subset=["respondent_id", "question"], keep="first")
    data["response_date"] = data["response_date"].dt.strftime("%Y-%m-%d")
    data = data.sort_values(["response_date", "respondent_id"]).reset_index(drop=True)
    summary = {"input_rows": original_rows, "clean_rows": len(data), "removed_rows": original_rows - len(data)}
    if data.empty:
        raise ValueError("No valid responses remain after cleaning. Check dates, options, and required fields.")
    return data, summary


def build_analysis(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return overall counts/shares, region shares, age shares, and daily trend."""
    counts = data["selected_option"].value_counts().reindex(OPTIONS, fill_value=0)
    overall = pd.DataFrame({"selected_option": OPTIONS, "votes": counts.values})
    overall["share_percent"] = (overall["votes"] / len(data) * 100).round(2)
    region = pd.crosstab(data["region"], data["selected_option"], normalize="index").reindex(columns=OPTIONS, fill_value=0).mul(100).round(2)
    age = pd.crosstab(data["age_group"], data["selected_option"], normalize="index").reindex(index=AGE_GROUPS, columns=OPTIONS, fill_value=0).mul(100).round(2)
    trend = (data.assign(response_date=pd.to_datetime(data["response_date"]))
             .groupby(["response_date", "selected_option"]).size().unstack(fill_value=0)
             .reindex(columns=OPTIONS, fill_value=0).sort_index())
    return overall, region, age, trend


def create_charts(overall: pd.DataFrame, region: pd.DataFrame, age: pd.DataFrame,
                  trend: pd.DataFrame, out: Path) -> None:
    """Save presentation-ready PNG charts in the output folder."""
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold", "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(overall.selected_option, overall.votes, color=COLORS)
    ax.bar_label(bars, labels=[f"{v}\n({p:.1f}%)" for v, p in zip(overall.votes, overall.share_percent)], padding=4, fontsize=9)
    ax.set(title="Poll results by option", ylabel="Responses", ylim=(0, max(overall.votes.max() * 1.22, 1)))
    fig.tight_layout(); fig.savefig(out / "option_votes.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 6))
    nonzero = overall[overall.votes > 0]
    ax.pie(nonzero.votes, labels=nonzero.selected_option, autopct="%1.1f%%", startangle=90,
           colors=[COLORS[OPTIONS.index(o)] for o in nonzero.selected_option], wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax.set_title("Share of responses by option", fontweight="bold")
    fig.tight_layout(); fig.savefig(out / "option_share.png", dpi=180); plt.close(fig)

    for matrix, title, filename in [(region, "Option share by region", "region_comparison.png"),
                                    (age, "Option share by age group", "age_comparison.png")]:
        fig, ax = plt.subplots(figsize=(9, 5))
        matrix.plot(kind="bar", stacked=True, ax=ax, color=COLORS, width=.72)
        ax.set(title=title, ylabel="Share of responses (%)", xlabel="", ylim=(0, 100))
        ax.legend(title="Selected option", bbox_to_anchor=(1.02, 1), loc="upper left")
        ax.tick_params(axis="x", rotation=0)
        fig.tight_layout(); fig.savefig(out / filename, dpi=180, bbox_inches="tight"); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    trend.plot(ax=ax, color=COLORS, linewidth=2)
    ax.set(title="Daily responses over time", ylabel="Responses", xlabel="Response date")
    ax.legend(title="Selected option", ncol=4, loc="upper left")
    fig.tight_layout(); fig.savefig(out / "daily_trend.png", dpi=180); plt.close(fig)


def create_insights(data: pd.DataFrame, overall: pd.DataFrame, region: pd.DataFrame,
                    age: pd.DataFrame, clean_summary: dict[str, int], out: Path) -> str:
    """Write plain-language, descriptive findings without implying causation."""
    leader = overall.sort_values(["votes", "selected_option"], ascending=[False, True]).iloc[0]
    region_leaders = region.idxmax(axis=1)
    age_leaders = age.idxmax(axis=1)
    date_span = f"{data.response_date.min()} to {data.response_date.max()}"
    lines = [
        "POLL RESULTS VISUALIZER — SUMMARY", "=" * 42,
        f"Question: {data.question.iloc[0]}",
        f"Valid responses: {len(data):,} | Date range: {date_span}",
        f"Cleaning: {clean_summary['input_rows']:,} input rows, {clean_summary['clean_rows']:,} retained, {clean_summary['removed_rows']:,} removed.", "",
        f"Overall leader: {leader.selected_option} with {int(leader.votes):,} responses ({leader.share_percent:.1f}%).",
        f"Runner-up: {overall.sort_values('votes', ascending=False).iloc[1].selected_option} ({overall.sort_values('votes', ascending=False).iloc[1].share_percent:.1f}%).",
        "Segment leaders (highest within-group share):",
    ]
    lines += [f"  Region — {segment}: {option} ({region.loc[segment, option]:.1f}%)" for segment, option in region_leaders.items()]
    lines += [f"  Age — {segment}: {option} ({age.loc[segment, option]:.1f}%)" for segment, option in age_leaders.items()]
    lines += ["", "Interpretation: These results describe this dataset only. Segment differences are descriptive, and synthetic demo data is fictional; do not generalize to a population without a representative sampling design."]
    report = "\n".join(lines)
    (out / "insights.txt").write_text(report + "\n", encoding="utf-8")
    return report


def run_analysis(input_path: Path | None = None, output_dir: Path = Path("outputs"),
                 data_dir: Path = Path("data"), respondents: int = 600, seed: int = 42) -> None:
    """Run the complete workflow and export cleaned data, tables, charts, and insights."""
    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    if input_path:
        raw = pd.read_csv(input_path)
        print(f"Loaded {len(raw):,} rows from {input_path}")
    else:
        raw = generate_synthetic_data(respondents, seed)
        demo_path = data_dir / "poll_responses.csv"
        raw.to_csv(demo_path, index=False)
        print(f"Generated fictional demo data: {demo_path}")
    clean, cleaning = clean_data(raw)
    overall, region, age, trend = build_analysis(clean)
    clean.to_csv(output_dir / "cleaned_responses.csv", index=False)
    overall.to_csv(output_dir / "option_summary.csv", index=False)
    region.rename_axis("region").to_csv(output_dir / "region_share.csv")
    age.rename_axis("age_group").to_csv(output_dir / "age_group_share.csv")
    trend.rename_axis("response_date").to_csv(output_dir / "daily_trend.csv")
    create_charts(overall, region, age, trend, output_dir)
    report = create_insights(clean, overall, region, age, cleaning, output_dir)
    print("\n" + report)
    print(f"\nSaved tables, charts, and insights to {output_dir.resolve()}")
