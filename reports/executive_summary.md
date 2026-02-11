# Executive Summary

## Problem
Student attrition creates academic and financial risk. This pipeline operationalizes risk detection and intervention planning using weekly student behavior signals.

## Approach
We run an end-to-end workflow: ETL -> feature engineering -> model training/evaluation -> latest risk scoring -> BI marts -> alerting -> offline A/B simulation -> ROI sensitivity.

## Results Snapshot
- AUC: **0.993**
- PR AUC: **0.994**
- Precision@0.5: **0.962**
- Recall@0.5: **0.954**

## Alerting
See `outputs/alerts/alert_latest.md` for threshold and week-over-week spike checks plus high-risk student list.

## Experiment + ROI
- Offline A/B scenarios are in `reports/ab_test_report.md`.
- ROI sensitivity grid is in `reports/roi_sensitivity.csv`.
- Example ROI row: uplift=10%, cost=50.0, roi=3500.00.

## Next Steps
1. Connect marts to Power BI for stakeholder monitoring.
2. Replace offline simulation with production randomized controlled trial.
3. Add model drift monitoring and retraining cadence.

---
Generated on 2026-02-11T23:10:05.010396Z | Demo mode: True
