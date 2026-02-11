"""Build BI-ready marts from model outputs."""
from __future__ import annotations

import pandas as pd

from src.config import PipelineConfig


def build_marts(latest_predictions: pd.DataFrame, config: PipelineConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    student_risk_latest = latest_predictions[
        ["id_student", "code_module", "week", "risk_score", "high_risk_flag", "weekly_score_mean", "cum_submissions"]
    ].copy()

    course_summary_latest = (
        student_risk_latest.groupby("code_module", as_index=False)
        .agg(
            student_count=("id_student", "nunique"),
            avg_risk_score=("risk_score", "mean"),
            high_risk_rate=("high_risk_flag", "mean"),
        )
        .sort_values("high_risk_rate", ascending=False)
    )

    student_risk_latest.to_csv(config.marts_dir / "student_risk_latest.csv", index=False)
    course_summary_latest.to_csv(config.marts_dir / "course_summary_latest.csv", index=False)
    return student_risk_latest, course_summary_latest
