@echo off
echo Initialisation de la base de donnees Django...
python manage.py makemigrations
python manage.py migrate
echo.
echo Base de donnees initialisee avec succes!
echo.
echo Pour creer un superutilisateur, executez:
echo python manage.py createsuperuser
pause

