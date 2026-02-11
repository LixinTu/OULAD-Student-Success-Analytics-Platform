# OULAD Student Success Prediction: Full-Stack Data Analyst / Data Scientist Portfolio Project

This project operationalizes student-risk analytics into a production-style workflow that an education organization can run daily: ingest data, engineer time-sliced features, train/evaluate a predictive model, publish BI-ready marts, trigger alerts, simulate intervention experiments, and estimate business ROI. It demonstrates analytics engineering + data science + stakeholder reporting in one reproducible repository.

## Executive Overview
Student dropout risk can be detected early from engagement and assessment behavior. This repository turns exploratory notebook work into an end-to-end analytics system that scores risk each run, publishes dashboards-ready outputs, raises operational alerts, and provides decision support (A/B simulation + ROI sensitivity) for intervention planning.

## Dataset Overview (OULAD)
- The Open University Learning Analytics Dataset (OULAD) contains student demographics, course interactions, and assessments.
- This pipeline expects raw CSVs in `data/raw/`:
  - `studentInfo.csv`
  - `studentAssessment.csv`
  - `assessments.csv`
- Engineered features represent weekly progression and performance:
  - rolling score averages,
  - cumulative submissions,
  - short-term score trend,
  - static demographic/context features.

## End-to-End Architecture
`Raw Data (CSV) -> ETL (extract/transform/load) -> Feature Engineering -> Model Training/Evaluation -> Latest Risk Prediction -> BI Marts -> Alerts + A/B Simulation + ROI -> Executive Report`

## Data Setup
### Option A: Run with real OULAD files
1. Create `data/raw/`.
2. Place the expected OULAD CSV files:
   - `studentInfo.csv`
   - `studentAssessment.csv`
   - `assessments.csv`
3. Run pipeline.

### Option B: Demo mode (for reviewers)
If files are missing, the pipeline automatically uses a small synthetic dataset and still generates complete outputs.

## How to Run
### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Run end-to-end (primary command)
```bash
bash run_pipeline.sh
```

Alternative:
```bash
make run
```

## What the Pipeline Produces
- `outputs/metrics_latest.json` (AUC, PR AUC, precision/recall, confusion matrix)
- `outputs/predictions_latest.csv` (risk scores for latest week)
- `outputs/marts/student_risk_latest.csv` (BI fact table)
- `outputs/marts/course_summary_latest.csv` (BI aggregate table)
- `outputs/alerts/alert_latest.md` (threshold + spike alerts)
- `outputs/experiments/assignment_latest.csv` (seeded A/B assignments)
- `reports/ab_test_report.md` (uplift scenarios + CIs + p-values)
- `reports/roi_sensitivity.csv` (ROI grid across uplift & intervention cost)
- `reports/executive_summary.md` (business summary)

## Experiment Design
- **Offline A/B Simulation**: top-K at-risk students are seeded-randomized into treatment/control.
- Simulated treatment uplift scenarios: **3%, 5%, 8%** pass-probability uplift.
- Statistical outputs:
  - pass rate difference,
  - bootstrap confidence intervals,
  - two-proportion z-test p-value.
- **Important**: this is offline simulation, not causal proof. A real randomized online intervention is the next step.

## Alerts Implemented
1. **Threshold alert**: triggers when high-risk proportion exceeds configured threshold.
2. **Spike alert**: triggers when mean risk score increases beyond configured week-over-week %.

Alert output includes trigger reason, summary stats, top 10 student IDs, and recommended actions.

## Outputs Gallery
- Marts: `outputs/marts/`
- Alerts: `outputs/alerts/alert_latest.md`
- Experiment report: `reports/ab_test_report.md`
- ROI sensitivity: `reports/roi_sensitivity.csv`
- Existing EDA image: `images/oulad_model_analysis.png`

## Repo Structure
```text
src/
  config.py
  pipeline.py
  utils/logging.py
  etl/{extract.py,transform.py,load.py}
  features/build_features.py
  model/{train.py,predict.py,evaluate.py}
  marts/build_marts.py
  alerts/alert.py
  experiments/ab_simulation.py
db/{schema.sql,marts.sql}
outputs/{marts,alerts,experiments,...}
reports/{executive_summary.md,ab_test_report.md,roi_sensitivity.csv}
dashboards/powerbi_refresh_guide.md
.github/workflows/daily_pipeline.yml
run_pipeline.sh
Makefile
.env.example
```

## Notebook Preservation
The original exploratory notebook is preserved:
- `oulad-student-success-prediction.ipynb`

## Future Improvements
- Replace file-based marts with warehouse tables (BigQuery/Snowflake/Postgres).
- Add model registry + drift monitoring + automated retraining gates.
- Move from offline simulation to live randomized interventions.
- Add causal inference methods (CUPED/uplift modeling) and heterogeneity analysis.
