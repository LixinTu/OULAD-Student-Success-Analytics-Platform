"""Prediction utilities for full-history risk scoring and snapshot views."""

from __future__ import annotations

import pandas as pd

from src.model.train import FEATURE_COLS


def predict_risk_timeseries(
    model: object, features: pd.DataFrame, high_risk_threshold: float
) -> pd.DataFrame:
    """Score risk for every weekly feature row."""
    scored = features.copy()
    scored["risk_score"] = model.predict_proba(scored[FEATURE_COLS])[:, 1]
    scored["high_risk_flag"] = (scored["risk_score"] >= high_risk_threshold).astype(int)
    return scored.sort_values(["week", "risk_score"], ascending=[True, False])


def select_prediction_snapshot(predictions: pd.DataFrame, current_week: int | None) -> pd.DataFrame:
    """Return latest-week snapshot, optionally overridden by CURRENT_WEEK."""
    if predictions.empty:
        return predictions.copy()

    max_week = int(predictions["week"].max())
    target_week = max_week if current_week is None else current_week
    snapshot = predictions[predictions["week"] == target_week].copy()
    if snapshot.empty:
        snapshot = predictions[predictions["week"] == max_week].copy()

    return snapshot.sort_values("risk_score", ascending=False)
