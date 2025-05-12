#!/bin/bash

# Remove the set -e to prevent early termination
# set -e

# Print Python version and environment info
echo "Python version:"
python --version
echo "Pip version:"
pip --version
echo "Environment variables:"
env | grep -v "PASSWORD\|SECRET\|KEY"
echo "Current directory:"
pwd
echo "Directory contents:"
ls -la

# Create static directory
mkdir -p static

# Run migrations
echo "Running migrations..."
python manage.py migrate --verbosity 2 || echo "Migration failed, continuing anyway"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing anyway"

# Check for errors
echo "Checking for deployment issues..."
python manage.py check --deploy || echo "Deployment check has issues, continuing anyway"

# Create a superuser if needed (will be skipped if the user already exists)
echo "Creating superuser if needed..."
python -c "
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.utils import IntegrityError

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created.')
    else:
        print('Superuser already exists.')
except Exception as e:
    print(f'Error creating superuser: {e}')
" || echo "Superuser creation failed, continuing anyway"

# Determine port - use PORT env var or default to 8000
PORT="${PORT:-8000}"
echo "Starting server on port $PORT..."

# Start server
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --log-level debug 