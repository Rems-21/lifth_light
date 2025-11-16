#!/bin/bash
# Script de démarrage pour Django
set -e

# Installer les dépendances si nécessaire
if [ ! -d "venv" ]; then
    python -m pip install -r requirements.txt
fi

# Collecter les fichiers statiques
python manage.py collectstatic --noinput || true

# Exécuter les migrations
python manage.py migrate --noinput || true

# Créer le superutilisateur depuis les variables d'environnement (si définies)
python manage.py create_admin_from_env || true

# Démarrer Gunicorn
exec python -m gunicorn liftandlight.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120

