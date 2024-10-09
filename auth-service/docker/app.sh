#!/bin/bash

# Применяем миграции alembic
alembic upgrade head

# Запуск приложения с gunicorn
exec gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
