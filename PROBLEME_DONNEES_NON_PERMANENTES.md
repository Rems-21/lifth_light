# 🔴 Pourquoi les données ne sont pas permanentes ?

## 🎯 Causes possibles

### 1. **Base de données SQLite utilisée (PROBLÈME PRINCIPAL)** ⚠️

Si `DATABASE_URL` n'est **pas défini** dans Render, Django utilise SQLite par défaut. Sur Render, les fichiers SQLite sont **effacés à chaque redéploiement** !

**Vérification :**
1. Allez sur votre service web dans Render
2. Cliquez sur **"Environment"**
3. Vérifiez si `DATABASE_URL` existe

**Si `DATABASE_URL` n'existe pas :**
- ✅ Votre base de données PostgreSQL n'est pas connectée
- ✅ Django utilise SQLite (données perdues à chaque redéploiement)

---

### 2. **Base de données PostgreSQL en pause** ⏸️

Sur le plan **gratuit** de Render, les bases de données PostgreSQL sont mises en pause après **90 jours d'inactivité**. Les données peuvent être perdues.

**Vérification :**
1. Allez sur votre base de données dans Render
2. Vérifiez le statut : **"Available"** ou **"Paused"** ?

**Si "Paused" :**
- Cliquez sur **"Resume"**
- Attendez 1-2 minutes
- Les données peuvent avoir été supprimées (limitation du plan gratuit)

---

### 3. **Migrations non exécutées** 📊

Les tables ne sont pas créées dans la base de données PostgreSQL.

**Vérification :**
Dans le Shell Render :
```bash
python manage.py showmigrations
```

Si vous voyez des `[ ]` (non migrées), les tables n'existent pas !

---

## ✅ SOLUTIONS

### Solution 1 : Connecter PostgreSQL (OBLIGATOIRE)

#### Étape 1 : Vérifier que la base existe

1. Dans Render Dashboard, vérifiez si `liftandlight-db` existe
2. Si elle n'existe pas, créez-la :
   - **"New +"** → **"PostgreSQL"**
   - Plan : **Free**
   - Nom : `liftandlight-db`

#### Étape 2 : Connecter la base au service web

**Méthode : Ajouter Manuellement `DATABASE_URL`** ✅

Le bouton "Link Database" n'est pas toujours visible dans Render. Voici la méthode manuelle qui fonctionne toujours :

1. **Allez sur votre base de données** `liftandlight-db` dans Render Dashboard
2. **Trouvez l'URL de connexion** :
   - Regardez dans l'onglet **"Info"** ou **"Connections"**
   - Cherchez **"Internal Database URL"** ou **"Connection String"**
   - L'URL ressemble à : `postgresql://user:password@hostname:port/database`
   - **Copiez cette URL complète** (tout le texte)
3. **Allez sur votre service web** → **"Environment"** (ou **"Settings"** → **"Environment"**)
4. **Ajoutez une nouvelle variable** :
   - Cliquez sur **"Add Environment Variable"** ou **"Add Variable"**
   - **Key** : `DATABASE_URL` (en majuscules, exactement comme ça)
   - **Value** : Collez l'URL que vous avez copiée
5. **Cliquez sur "Save Changes"** ou **"Save"**
6. **Redéployez votre service** (Render le fera automatiquement ou cliquez sur "Manual Deploy")

**Important :** 
- ✅ Le nom de la variable doit être exactement `DATABASE_URL` (majuscules)
- ✅ Collez l'URL complète (commence par `postgresql://`)
- ✅ Ne modifiez pas l'URL, copiez-la telle quelle

#### Étape 3 : Vérifier la connexion

Dans le Shell Render :
```bash
python manage.py dbshell
```

Si ça fonctionne, vous verrez : `psql (PostgreSQL ...)`
Tapez `\q` pour quitter.

---

### Solution 2 : Exécuter les migrations

Une fois PostgreSQL connecté, exécutez les migrations :

```bash
# Dans le Shell Render
python manage.py migrate
```

Vérifiez que tout est migré :
```bash
python manage.py showmigrations
```

Tous les modèles devraient être marqués `[X]`.

---

### Solution 3 : Vérifier que settings_prod est utilisé

Assurez-vous que `DJANGO_SETTINGS_MODULE=liftandlight.settings_prod` est défini dans Environment.

Votre `settings_prod.py` utilise PostgreSQL si `DATABASE_URL` existe :
```python
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Utilise PostgreSQL ✅
else:
    # Utilise SQLite (données perdues) ❌
```

---

## 🔍 Diagnostic complet

### Checklist de vérification

1. ✅ **Base de données PostgreSQL créée** dans Render
2. ✅ **`DATABASE_URL` existe** dans Environment du service web
3. ✅ **`DJANGO_SETTINGS_MODULE=liftandlight.settings_prod`** est défini
4. ✅ **Base de données est "Available"** (pas "Paused")
5. ✅ **Migrations exécutées** (`python manage.py migrate`)
6. ✅ **Tables créées** (`python manage.py showmigrations`)

---

## 🧪 Test de persistance

### Test 1 : Créer des données

1. Connectez-vous à l'admin : `https://votre-app.onrender.com/admin/`
2. Créez un article de blog ou un projet
3. Notez l'ID ou le titre

### Test 2 : Redéployer

1. Dans Render, cliquez sur **"Manual Deploy"** → **"Deploy latest commit"**
2. Attendez la fin du déploiement

### Test 3 : Vérifier

1. Reconnectez-vous à l'admin
2. Vérifiez si vos données existent toujours

**Si les données existent :** ✅ PostgreSQL fonctionne !
**Si les données ont disparu :** ❌ SQLite est utilisé ou base en pause

---

## ⚠️ Limitations du plan gratuit Render

### Base de données PostgreSQL Free

- ✅ **90 jours d'inactivité** → Base mise en pause
- ⚠️ **Données peuvent être supprimées** après pause prolongée
- ⚠️ **Limite de 1 GB** de données
- ⚠️ **Pas de backup automatique**

### Recommandations

1. **Utilisez régulièrement votre site** (au moins une fois par mois)
2. **Faites des backups manuels** si possible
3. **Upgrade vers Starter ($7/mois)** pour :
   - Base de données toujours active
   - Backups automatiques
   - Plus de stockage

---

## 🛠️ Script de vérification

Créez un fichier `check_db.py` pour vérifier la connexion :

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liftandlight.settings_prod')
django.setup()

from django.db import connection

print("=== Vérification Base de Données ===")
print(f"Engine: {connection.settings_dict['ENGINE']}")
print(f"Name: {connection.settings_dict.get('NAME', 'N/A')}")

if 'postgresql' in connection.settings_dict['ENGINE']:
    print("✅ PostgreSQL connecté - Données permanentes")
else:
    print("❌ SQLite utilisé - Données NON permanentes")
```

Exécutez dans le Shell Render :
```bash
python check_db.py
```

---

## 📝 Résumé

**Pour que les données soient permanentes :**

1. ✅ **Créez PostgreSQL** dans Render
2. ✅ **Connectez-la** au service web (`DATABASE_URL`)
3. ✅ **Exécutez les migrations** (`python manage.py migrate`)
4. ✅ **Vérifiez** que la base est "Available" (pas "Paused")
5. ✅ **Utilisez régulièrement** votre site (plan gratuit)

**Si vous suivez ces étapes, vos données seront permanentes !** 🎉

---

## 🆘 Si le problème persiste

1. **Vérifiez les logs** de Render pour les erreurs
2. **Vérifiez que `DATABASE_URL` est bien défini** dans Environment
3. **Testez la connexion** avec `python manage.py dbshell`
4. **Contactez le support Render** si nécessaire

