# Power BI Refresh Guide

## Files to Connect
Use **Get Data -> Text/CSV** (or Folder) and import:
- `outputs/marts/student_risk_daily_sample.csv`
- `outputs/marts/course_summary_daily_sample.csv`
- `outputs/predictions_latest.csv` (optional latest-week detail table)

`student_risk_daily` and `course_summary_daily` are full-history weekly marts with `run_date` + `week`.

## Recommended Model / Star Schema
- **FactStudentRisk**: `student_risk_daily_sample`
- **FactCourseSummary**: `course_summary_daily_sample`
- **DimCourse**: distinct `code_module`
- Optional dimensions: student demographics from processed tables.

Relationships:
- `FactStudentRisk[code_module]` -> `DimCourse[code_module]`
- `FactCourseSummary[code_module]` -> `DimCourse[code_module]`

## Suggested Visuals
1. Risk score distribution histogram (latest `run_date` filter optional).
2. High-risk rate KPI card with threshold indicator.
3. Weekly trend line: Axis=`week`, Values=`avg_risk_score`, Legend=`run_date`.
4. Top courses by weekly high-risk rate (clustered bar, slicer on week).
5. Top at-risk student table from `predictions_latest.csv`.

## Refresh Approach
- **Local refresh**: rerun `bash run_pipeline.sh`, then click Refresh in Desktop.
- **Service refresh idea**: store outputs in OneDrive/SharePoint or database; schedule Power BI dataset refresh after GitHub Action run.
