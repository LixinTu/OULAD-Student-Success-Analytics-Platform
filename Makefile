.PHONY: run run-demo compile lint format test check docker-up verify-postgres

run:
	python -m src.pipeline --demo

run-demo:
	python -m src.pipeline --demo

compile:
	python -m compileall src

lint:
	ruff check src tests
	black --check src tests

format:
	black src tests
	ruff check --fix src tests

test:
	pytest -q

check: compile lint test

docker-up:
	docker compose up --build

verify-postgres:
	docker compose exec -T postgres psql -U oulad -d oulad_analytics -c "\dt"
	docker compose exec -T postgres psql -U oulad -d oulad_analytics -c "SELECT 'student_risk_daily' AS table_name, COUNT(*) AS row_count FROM student_risk_daily UNION ALL SELECT 'course_summary_daily', COUNT(*) FROM course_summary_daily UNION ALL SELECT 'experiment_results', COUNT(*) FROM experiment_results UNION ALL SELECT 'alert_log', COUNT(*) FROM alert_log;"
	docker compose exec -T postgres psql -U oulad -d oulad_analytics -c "select min(week), max(week), count(distinct week) from student_risk_daily;"
	docker compose exec -T postgres psql -U oulad -d oulad_analytics -c "select week, count(*) from student_risk_daily group by week order by week limit 20;"
	docker compose exec -T postgres psql -U oulad -d oulad_analytics -c "select min(week), max(week), count(*) from course_summary_daily;"
	docker compose exec -T postgres psql -U oulad -d oulad_analytics -c "select week, count(*) from course_summary_daily group by week order by week limit 20;"
