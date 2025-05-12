#!/bin/bash

# Exit on error
set -e

echo "Checking Python and pip versions..."
python --version || python3 --version

# Try multiple ways to install pip if needed
if ! command -v pip &> /dev/null; then
    echo "Pip not found, trying to install..."
    apt-get update && apt-get install -y python3-pip || true
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py || python3 get-pip.py || echo "Couldn't install pip, continuing anyway"
fi

# Install Python dependencies
echo "Installing dependencies..."
pip install --upgrade pip || python -m pip install --upgrade pip || python3 -m pip install --upgrade pip || echo "Pip upgrade failed, continuing anyway"
pip install -r requirements.txt || python -m pip install -r requirements.txt || python3 -m pip install -r requirements.txt

# Create static directory
echo "Creating static directory..."
mkdir -p static

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || python3 manage.py collectstatic --noinput || echo "Collectstatic failed, continuing anyway" 