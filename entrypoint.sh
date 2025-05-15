#!/bin/bash

# Set error handling
set -e

# Print environment information (for debugging)
echo "👉 Environment: $RAILWAY_ENVIRONMENT"
echo "👉 Project: $RAILWAY_PROJECT_NAME"
echo "👉 Service: $RAILWAY_SERVICE_NAME"

# Make sure Python outputs everything immediately
export PYTHONUNBUFFERED=1

# Load environment variables
if [ -f .env ]; then
    echo "🔄 Loading environment variables from .env file"
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run database migrations
echo "🏁 Running database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if environment variables are provided
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Creating/updating superuser..."
    python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created successfully!')
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.email = email
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print('Superuser updated successfully!')
"
fi

# Start Gunicorn server
echo "🚀 Starting Gunicorn server..."
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT 