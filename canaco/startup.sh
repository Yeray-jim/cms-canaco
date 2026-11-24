#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput --email "${DJANGO_SUPERUSER_EMAIL:-admin@canaco.local}" || true
fi

gunicorn canaco.wsgi:application --bind 0.0.0.0:8000
