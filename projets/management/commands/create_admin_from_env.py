"""
Django management command to create superuser from environment variables
Usage: python manage.py create_admin_from_env
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables (ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Variables d\'environnement manquantes. '
                    'Définissez ADMIN_USERNAME, ADMIN_EMAIL et ADMIN_PASSWORD.'
                )
            )
            return

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'L\'utilisateur "{username}" existe déjà.')
            )
            return

        # Créer le superutilisateur
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superutilisateur "{username}" créé avec succès!'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de la création: {str(e)}')
            )

