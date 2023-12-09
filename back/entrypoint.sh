#!/bin/bash

# Выполнение миграций Alembic
alembic upgrade head

# Запуск FastAPI приложения
uvicorn main:app --host 0.0.0.0 --port 5000
