#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Seed the reference content the first time the database is empty. Safe to run on
# every deploy: each command exits immediately once its content exists, so editors
# keep full control afterwards. The "|| true" keeps a content problem from failing the deploy.
python manage.py load_program_structure --if-unseeded || true
python manage.py load_projects --if-unseeded || true
python manage.py seed_program_gallery || true

exec gunicorn lacd_project.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers ${WEB_CONCURRENCY:-2} --timeout 120 --access-logfile - --error-logfile -
