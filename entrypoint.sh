#!/usr/bin/env bash
set -e
cd online
python manage.py migrate
python -m celery -A online worker
python manage.py runserver 0.0.0.0:8000