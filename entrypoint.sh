#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print Python version
echo "Python version:"
python --version || python3 --version

# Create static directory if it doesn't exist
mkdir -p static

# Run collectstatic (ignore errors)
echo "Collecting static files..."
python manage.py collectstatic --noinput || python3 manage.py collectstatic --noinput || echo "Collectstatic failed, continuing anyway"

# Run migrations (ignore errors)
echo "Running migrations..."
python manage.py migrate || python3 manage.py migrate || echo "Migration failed, continuing anyway"

# Determine port - use PORT env var or default to 8000
PORT="${PORT:-8000}"
echo "Starting server on port $PORT..."

# Start server
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT 