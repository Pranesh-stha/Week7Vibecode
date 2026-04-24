#!/bin/sh
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Loading initial data..."
python manage.py loaddata rentals/fixtures/initial_data.json || true

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@driveeasy.com', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
"

echo "Starting server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
