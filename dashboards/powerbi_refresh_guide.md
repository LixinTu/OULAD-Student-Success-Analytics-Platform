# Power BI Refresh Guide

## Files to Connect
Use **Get Data -> Text/CSV** (or Folder) and import:
- `outputs/marts/student_risk_latest.csv`
- `outputs/marts/course_summary_latest.csv`
- `outputs/predictions_latest.csv` (optional detail table)

## Recommended Model / Star Schema
- **FactStudentRisk**: `student_risk_latest`
- **DimCourse**: distinct `code_module`
- Optional dimensions: student demographics from processed tables.

Relationships:
- `FactStudentRisk[code_module]` -> `DimCourse[code_module]`

## Suggested Visuals
1. Risk score distribution histogram.
2. High-risk rate KPI card with threshold indicator.
3. Week-over-week trend line of average risk.
4. Top courses by high-risk rate (bar chart).
5. Top at-risk student table with slicers for course/cohort.

## Refresh Approach
- **Local refresh**: rerun `bash run_pipeline.sh`, then click Refresh in Desktop.
- **Service refresh idea**: store outputs in OneDrive/SharePoint or database; schedule Power BI dataset refresh after GitHub Action run.
