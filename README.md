# OULAD Student Success Prediction System

Machine learning-based student performance prediction with time-slicing feature engineering

## Overview

Student success prediction model built on OULAD dataset using time-slicing and innovative feature engineering to predict student academic outcomes at day 90 of the course.

## Model Performance

![Model Performance](images/oulad_model_analysis.png)

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.945 |
| Accuracy | 88.2% |
| Recall | 95.2% |
| F1-Score | 0.93 |

## Core Features

1. **Total Clicks**: Cumulative clicks up to day 90
2. **Learning Stability**: Standard deviation of daily clicks (innovative feature)
3. **Early Preview**: Clicks before course start
4. **Recent Trend**: Clicks between day 60-90
5. **Assignment Performance**: Average score and submission count

## Tech Stack

- Python 3.8+
- XGBoost
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn

## Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Prepare Data

Download OULAD dataset:
- studentInfo.csv
- studentVle.csv
- studentAssessment.csv

Dataset: https://www.kaggle.com/datasets/anlgrbz/student-demographics-online-education-dataoulad

### Run Model

```bash
python oulad_english_version.py
```

Or run directly in Kaggle Notebook.

## Feature Importance

XGBoost feature importance ranking:

1. Assignment submission count (most important)
2. Recent trend clicks
3. Average assignment score
4. Learning stability (std)
5. Total clicks
6. Early preview clicks

## Project Structure

```
OULAD-Student-Success-Prediction/
├── oulad_english_version.py
├── README.md
├── requirements.txt
├── .gitignore
└── images/
    └── oulad_model_analysis.png
```

## Model Configuration

```python
XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8
)
```

## Resume Description Templates

**Technical Focus**
```
OULAD Student Success Prediction System (ROC-AUC: 0.945)
- Designed 5 time-series features including learning stability for 90-day early prediction
- Built XGBoost model with 88.2% accuracy for student performance prediction
- Tech Stack: Python, XGBoost, Scikit-learn, Pandas
```

**Business Focus**
```
Student Academic Performance Prediction System
- Built ML model on 32,000+ student records, achieving ROC-AUC 0.945
- Identified assignment behavior and recent learning status as key success indicators
- Enabled mid-course accurate prediction for early intervention
```

## Dataset

- Source: Open University, UK
- Scale: 32,593 students, 22 courses
- Period: 2013-2014 academic year

## References

1. Kuzilek, J., et al. (2017). Open university learning analytics dataset. Scientific Data, 4(1), 1-8.
2. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. KDD'16.

## License

MIT License
