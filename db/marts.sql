-- Example mart-level query patterns
SELECT code_module,
       student_count,
       avg_risk_score,
       high_risk_rate
FROM course_summary_latest
ORDER BY high_risk_rate DESC;

SELECT *
FROM student_risk_latest
WHERE high_risk_flag = 1
ORDER BY risk_score DESC
LIMIT 50;
