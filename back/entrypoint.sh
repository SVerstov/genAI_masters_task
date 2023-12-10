#!/bin/bash

# Выполнение миграций Alembic
alembic upgrade head

# Запуск FastAPI приложения
python main.py
