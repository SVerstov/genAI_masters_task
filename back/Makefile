.PHONY: init migrate migrations downgrade

init:
	python -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

migrate:
	alembic upgrade head

migrations:
	alembic revision --autogenerate -m "$(word 2,$(MAKECMDGOALS))"

downgrade:
	alembic downgrade -1
