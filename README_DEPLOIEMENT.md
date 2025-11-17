# Guide de Déploiement

Ce projet Django peut être déployé sur plusieurs plateformes. Voici les meilleures options, classées par facilité :

## 🥇 1. Render (RECOMMANDÉ - Le plus simple)

**Voir** `RENDER_DEPLOIEMENT.md` pour le guide complet et détaillé sur Render.

**Avantages :**
- ✅ Plan gratuit disponible
- ✅ Base de données PostgreSQL incluse
- ✅ Déploiement automatique depuis GitHub
- ✅ Configuration via `render.yaml` (déjà créé)

---

## 🥈 2. Railway (Alternative)

**Avantages :**
- ✅ Plan gratuit disponible
- ✅ Base de données PostgreSQL incluse
- ✅ Déploiement automatique depuis GitHub
- ✅ Configuration via `render.yaml` (déjà créé)

**Note :** Railway n'est plus la méthode recommandée. Utilisez Render à la place (voir ci-dessus).

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

## 🚀 Déploiement rapide (Render)

**Le plus rapide :**

1. Allez sur https://render.com
2. "New +" → "Blueprint"
3. Connectez votre repo GitHub : `Rems-21/lifth_light`
4. Render détectera automatiquement `render.yaml`
5. Cliquez sur "Apply"
6. C'est tout ! 🎉

Render créera automatiquement :
- ✅ Le service web
- ✅ La base de données PostgreSQL
- ✅ Les variables d'environnement
- ✅ Exécutera les migrations

**Voir** `RENDER_DEPLOIEMENT.md` pour plus de détails.

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

