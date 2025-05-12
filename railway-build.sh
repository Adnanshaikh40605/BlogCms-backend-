#!/bin/bash

# Print Python version to verify what we're using
python --version

# Install dependencies
pip install -r requirements.txt

# Create static directory
mkdir -p static

# Collect static files
python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing anyway"

echo "Build completed successfully!" 