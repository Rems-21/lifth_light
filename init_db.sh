#!/bin/bash
echo "Initialisation de la base de données Django..."
python manage.py makemigrations
python manage.py migrate
echo ""
echo "Base de données initialisée avec succès!"
echo ""
echo "Pour créer un superutilisateur, exécutez:"
echo "python manage.py createsuperuser"

