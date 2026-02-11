"""Main orchestration for end-to-end OULAD analytics pipeline."""
from __future__ import annotations

import argparse
import json
from datetime import datetime

from src.alerts.alert import generate_alert
from src.config import ensure_directories, load_config
from src.etl.extract import extract_data
from src.etl.load import load_processed_data
from src.etl.transform import transform_data
from src.experiments.ab_simulation import run_ab_simulation
from src.features.build_features import build_time_sliced_features
from src.marts.build_marts import build_marts
from src.model.evaluate import evaluate_model
from src.model.predict import predict_latest_risk
from src.model.train import train_model
from src.utils.logging import get_logger

logger = get_logger(__name__)


def write_executive_summary(metrics: dict, alert_text: str, roi_topline: dict, demo_mode: bool) -> None:
    config = load_config(demo_mode=demo_mode)
    summary = f"""# Executive Summary

## Problem
Student attrition creates academic and financial risk. This pipeline operationalizes risk detection and intervention planning using weekly student behavior signals.

## Approach
We run an end-to-end workflow: ETL -> feature engineering -> model training/evaluation -> latest risk scoring -> BI marts -> alerting -> offline A/B simulation -> ROI sensitivity.

## Results Snapshot
- AUC: **{metrics['auc']:.3f}**
- PR AUC: **{metrics['pr_auc']:.3f}**
- Precision@0.5: **{metrics['precision_at_0_5']:.3f}**
- Recall@0.5: **{metrics['recall_at_0_5']:.3f}**

## Alerting
See `outputs/alerts/alert_latest.md` for threshold and week-over-week spike checks plus high-risk student list.

## Experiment + ROI
- Offline A/B scenarios are in `reports/ab_test_report.md`.
- ROI sensitivity grid is in `reports/roi_sensitivity.csv`.
- Example ROI row: uplift={roi_topline['uplift_assumption']:.0%}, cost={roi_topline['cost_per_student']}, roi={roi_topline['roi']:.2f}.

## Next Steps
1. Connect marts to Power BI for stakeholder monitoring.
2. Replace offline simulation with production randomized controlled trial.
3. Add model drift monitoring and retraining cadence.

---
Generated on {datetime.utcnow().isoformat()}Z | Demo mode: {demo_mode}
"""
    (config.reports_dir / "executive_summary.md").write_text(summary)


def run_pipeline(demo_mode: bool) -> None:
    config = load_config(demo_mode=demo_mode)
    ensure_directories(config)

    logger.info("Starting pipeline")
    student_info, student_assessment, assessments = extract_data(config)
    clean_df = transform_data(student_info, student_assessment, assessments)
    load_processed_data(clean_df, config)

    features = build_time_sliced_features(clean_df)
    model, _, _, X_test, y_test = train_model(features, config)
    metrics = evaluate_model(model, X_test, y_test, config)

    latest_predictions = predict_latest_risk(model, features, config.current_week)
    latest_predictions.to_csv(config.outputs_dir / "predictions_latest.csv", index=False)

    build_marts(latest_predictions, config)
    alert_text = generate_alert(latest_predictions, features, config)
    _, _, roi_df = run_ab_simulation(latest_predictions, config)

    roi_topline = roi_df.sort_values("roi", ascending=False).iloc[0].to_dict()
    write_executive_summary(metrics, alert_text, roi_topline, demo_mode=demo_mode)

    logger.info("Pipeline completed successfully")
    logger.info(json.dumps({"metrics": metrics, "best_roi": roi_topline}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OULAD end-to-end pipeline")
    parser.add_argument("--demo", action="store_true", help="Force demo mode with synthetic data")
    args = parser.parse_args()
    run_pipeline(demo_mode=args.demo)
