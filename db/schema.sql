-- Core schema reference for analytics pipeline
CREATE TABLE IF NOT EXISTS student_risk_latest (
    id_student INTEGER,
    code_module TEXT,
    week INTEGER,
    risk_score DOUBLE PRECISION,
    high_risk_flag INTEGER,
    weekly_score_mean DOUBLE PRECISION,
    cum_submissions DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS course_summary_latest (
    code_module TEXT,
    student_count INTEGER,
    avg_risk_score DOUBLE PRECISION,
    high_risk_rate DOUBLE PRECISION
);
