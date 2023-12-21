#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."

wait-for-it db:5432 --timeout=5 --strict -- echo "PostgreSQL ready"

echo "Running migrations..."
python manage.py migrate

python manage.py runserver 0.0.0.0:8000