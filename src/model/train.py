"""Model training module."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from src.config import PipelineConfig

FEATURE_COLS = [
    "weekly_score_mean",
    "weekly_submissions",
    "studied_credits",
    "age_band_num",
    "imd_band_num",
    "disability_flag",
    "cum_submissions",
    "rolling_score_3w",
    "score_trend_2w",
]


def train_model(features: pd.DataFrame, config: PipelineConfig) -> tuple[object, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    model_df = features.dropna(subset=FEATURE_COLS + ["target_high_risk"]).copy()
    X = model_df[FEATURE_COLS]
    y = model_df["target_high_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=config.random_seed, stratify=y
    )

    model = LogisticRegression(max_iter=1000, random_state=config.random_seed)
    model.fit(X_train, y_train)

    joblib.dump(model, config.models_dir / "risk_model.joblib")
    metadata = {
        "model_type": "LogisticRegression",
        "feature_columns": FEATURE_COLS,
        "random_seed": config.random_seed,
    }
    Path(config.models_dir / "model_metadata.json").write_text(json.dumps(metadata, indent=2))
    return model, X_train, y_train, X_test, y_test
