"""
Script pour créer automatiquement un superutilisateur Django
à partir des variables d'environnement
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liftandlight.settings_prod')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Récupérer les variables d'environnement
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', None)

# Vérifier si un mot de passe est fourni
if not ADMIN_PASSWORD:
    print("⚠️  ADMIN_PASSWORD non défini. Superutilisateur non créé.")
    print("   Pour créer un admin automatiquement, ajoutez ADMIN_PASSWORD dans les variables d'environnement.")
    sys.exit(0)

# Vérifier si le superutilisateur existe déjà
if User.objects.filter(username=ADMIN_USERNAME).exists():
    print(f"✅ Superutilisateur '{ADMIN_USERNAME}' existe déjà.")
    # Optionnel : mettre à jour le mot de passe si ADMIN_PASSWORD est défini
    user = User.objects.get(username=ADMIN_USERNAME)
    user.set_password(ADMIN_PASSWORD)
    user.email = ADMIN_EMAIL
    user.save()
    print(f"   Mot de passe et email mis à jour.")
else:
    # Créer le superutilisateur
    try:
        User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD
        )
        print(f"✅ Superutilisateur créé avec succès !")
        print(f"   Username: {ADMIN_USERNAME}")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {'*' * len(ADMIN_PASSWORD)}")
    except Exception as e:
        print(f"❌ Erreur lors de la création du superutilisateur: {e}")
        sys.exit(1)

