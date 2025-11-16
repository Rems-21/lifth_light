#!/bin/bash
# Script de build pour collecter les fichiers statiques
set -e

echo "Installing dependencies..."
python -m pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput || true

echo "Build complete!"

