# Implementation Plan: Full-History Weekly Marts

## Objective
Refactor the pipeline to produce full historical weekly marts (weeks 0..max_week) instead of single-week snapshots, while preserving optional snapshot behavior for alerts and experiments.

## Files to edit and planned changes

### 1) `src/config.py`
- Make `CURRENT_WEEK` optional (`int | None`) instead of required int.
- Add helper parser for optional int env vars.
- Default `CURRENT_WEEK` to `None` when unset/empty.
- Keep `PIPELINE_DEMO_MODE` behavior unchanged.

### 2) `src/model/predict.py`
- Replace single-week prediction path with full-history prediction function over all rows.
- Add helper to derive a latest-week snapshot from full-history predictions:
  - If `CURRENT_WEEK` override is set, use that week when present.
  - Otherwise, resolve latest week as `max(features.week)`.
  - Fallback safely to max week if override is missing in data.
- Ensure predictions retain `week`, `id_student`, `code_module`, and feature columns needed by marts.

### 3) `src/marts/build_marts.py`
- Build `student_risk_daily` from full-history predictions (all weeks) with `run_date`.
- Build `course_summary_daily` grouped by `(run_date, week, code_module)`.
- Preserve existing columns, adding `week` to course summary.
- Continue writing CSV samples and inserting into DB.

### 4) `db/schema.sql`
- Add `week` column to `course_summary_daily` table schema for weekly trend aggregations.
- Keep existing columns for backward compatibility.

### 5) `src/pipeline.py`
- Use full-history prediction dataframe for marts.
- Compute latest-week snapshot from full-history predictions for:
  - alerts,
  - experiments/ROI,
  - optional `predictions_latest.csv` output.
- Ensure data flow:
  `extract -> transform -> features(all weeks) -> train(time split) -> predict(all weeks) -> marts(full history)`
  and separately snapshot for alert/experiment consumers.

### 6) `src/alerts/alert.py`
- Keep alert calculations on latest week snapshot input.
- Update function signature naming/doc intent to clarify snapshot use.
- Keep week-over-week logic based on full feature history.

### 7) `tests/test_pipeline_smoke.py`
- Extend smoke test assertions to verify multi-week marts:
  - `count(distinct week) > 1` in generated `student_risk_daily_sample.csv`.
  - `course_summary_daily_sample.csv` includes `week` and multiple distinct weeks.

### 8) `README.md`
- Update runbook and verification section with required SQL:
  - `select min(week), max(week), count(distinct week) from student_risk_daily;`
  - `select week, count(*) from student_risk_daily group by week order by week limit 20;`
- Add course summary min/max week checks and row-count checks.
- Clarify that marts are full-history time series while alerts/experiments may use latest-week snapshot.

### 9) `dashboards/powerbi_refresh_guide.md`
- Update Power BI guidance to use weekly trend visuals across `week` and `run_date` from full-history marts.

## Data flow after refactor
1. Build features for every `(id_student, code_module, week)`.
2. Train/evaluate with week-based split (`SPLIT_WEEK`) on full feature history.
3. Score all weekly rows to produce historical risk predictions.
4. Persist full-history marts with `run_date` + `week` granularity.
5. Derive latest-week snapshot only for alerting and top-K experiment simulation.

## Validation approach
- Run test suite (`pytest` smoke tests).
- Run pipeline locally in demo mode.
- Verify artifacts contain multiple weeks.
- Verify required SQL works against sqlite/postgres schema.

