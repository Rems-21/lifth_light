# Guide de Déploiement

Ce projet Django peut être déployé sur plusieurs plateformes. Voici les meilleures options, classées par facilité :

## 🥇 1. Railway (RECOMMANDÉ - Le plus simple)

**Avantages :**
- ✅ Gratuit au début (500$ de crédit/mois)
- ✅ Base de données PostgreSQL incluse
- ✅ Déploiement automatique depuis GitHub
- ✅ Configuration minimale requise
- ✅ Support Django natif

**Étapes :**

1. **Créer un compte** : https://railway.app
2. **Nouveau projet** → "Deploy from GitHub repo"
3. **Sélectionner votre dépôt** : `Rems-21/lifth_light`
4. **Ajouter une base de données** :
   - Cliquez sur "+ New" → "Database" → "PostgreSQL"
   - Railway créera automatiquement la variable `DATABASE_URL`
5. **Variables d'environnement** (dans Settings → Variables) :
   ```
   DJANGO_SETTINGS_MODULE=liftandlight.settings_prod
   SECRET_KEY=votre-cle-secrete-generee
   DEBUG=False
   ```
   
   **IMPORTANT** : Utilisez `settings_prod` pour la production (WhiteNoise configuré pour les fichiers statiques)
6. **Déploiement** : Railway détecte automatiquement `Procfile` et déploie !

**Générer SECRET_KEY :**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Migration de la base de données :**
Railway exécute automatiquement les migrations. Si nécessaire, dans le terminal Railway :
```bash
python manage.py migrate
python manage.py createsuperuser
```

**Note :** Si vous voyez l'erreur `gunicorn: command not found`, assurez-vous que `gunicorn>=21.2.0` est dans `requirements.txt`. Les fichiers de configuration utilisent `python -m gunicorn` pour garantir que gunicorn est trouvé.

---

## 🥈 2. Render (Gratuit, facile)

**Avantages :**
- ✅ Plan gratuit disponible
- ✅ Base de données PostgreSQL incluse
- ✅ Déploiement automatique depuis GitHub
- ✅ Configuration via `render.yaml` (déjà créé)

**Étapes :**

1. **Créer un compte** : https://render.com
2. **Nouveau "Web Service"** → Connecter votre dépôt GitHub
3. **Configuration** :
   - **Build Command** : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command** : `gunicorn liftandlight.wsgi`
   - **Environment** : `Python 3`
4. **Ajouter une base de données PostgreSQL** :
   - "New" → "PostgreSQL"
   - Render créera automatiquement `DATABASE_URL`
5. **Variables d'environnement** :
   ```
   DJANGO_SETTINGS_MODULE=liftandlight.settings
   SECRET_KEY=votre-cle-secrete
   DEBUG=False
   ```
6. **Déployer** : Render utilisera automatiquement `render.yaml`

---

## 🥉 3. DigitalOcean App Platform

**Avantages :**
- ✅ Support Django excellent
- ✅ Base de données incluse
- ✅ Plan gratuit avec limitations

**Étapes :**

1. **Créer un compte** : https://www.digitalocean.com
2. **App Platform** → "Create App" → Connecter GitHub
3. **Configuration automatique** : DigitalOcean détecte Django
4. **Ajouter une base de données** : PostgreSQL
5. **Variables d'environnement** : Comme ci-dessus

---

## ⚠️ 4. Vercel (Non recommandé pour Django)

Vercel est conçu pour les sites statiques et les fonctions serverless, pas pour les applications Django complètes. Les problèmes rencontrés sont normaux.

**Si vous voulez quand même utiliser Vercel :**
- Nécessite une base de données externe (Supabase, PlanetScale)
- Configuration complexe
- Limitations sur les fichiers statiques et média
- Pas de support natif pour Django

---

## 📋 Préparation avant déploiement

### 1. Générer une SECRET_KEY sécurisée

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Mettre à jour settings.py pour la production

Créez `liftandlight/settings_prod.py` :

```python
from .settings import *
import os

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com', '*.railway.app', '*.render.com']

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (utiliser Cloudinary ou S3 en production)
# MEDIA_URL = 'https://votre-cdn.com/media/'
```

### 3. Fichiers à vérifier

- ✅ `requirements.txt` - Dépendances Python
- ✅ `Procfile` - Commande de démarrage (Railway, Heroku)
- ✅ `runtime.txt` - Version Python
- ✅ `render.yaml` - Configuration Render
- ✅ `.gitignore` - Exclut `db.sqlite3`, `__pycache__`, etc.

---

## 🚀 Déploiement rapide (Railway)

**Le plus rapide :**

1. Allez sur https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Sélectionnez `lifth_light`
4. Railway détecte automatiquement Django
5. Ajoutez PostgreSQL dans le projet
6. Ajoutez `SECRET_KEY` dans les variables
7. C'est tout ! 🎉

Railway exécutera automatiquement :
- `pip install -r requirements.txt`
- `python manage.py migrate` (si configuré)
- `gunicorn liftandlight.wsgi`

---

## 📝 Notes importantes

1. **Base de données** : N'utilisez jamais SQLite en production. Utilisez PostgreSQL.
2. **Fichiers statiques** : WhiteNoise est déjà configuré dans `requirements.txt`
3. **Fichiers média** : Pour la production, utilisez Cloudinary, AWS S3, ou Cloudflare R2
4. **SECRET_KEY** : Ne jamais commiter la SECRET_KEY dans Git
5. **DEBUG** : Toujours mettre `DEBUG=False` en production

---

## 🆘 Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs de déploiement
2. Vérifiez les variables d'environnement
3. Vérifiez que la base de données est bien connectée
4. Exécutez `python manage.py migrate` manuellement si nécessaire

