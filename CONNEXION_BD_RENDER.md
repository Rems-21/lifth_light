# 🔌 Connexion Base de Données sur Render

## ✅ Configuration Automatique

Votre projet est **déjà configuré** pour se connecter automatiquement à PostgreSQL sur Render !

---

## 🎯 Comment ça fonctionne

### 1. Le fichier `render.yaml`

Votre `render.yaml` contient déjà la configuration de la base de données :

```yaml
services:
  - type: web
    name: liftandlight
    # ... autres configs ...
    database:
      name: liftandlight-db
      plan: free
      databaseName: liftandlight
      user: liftandlight
```

**Quand vous déployez via `render.yaml`, Render :**
- ✅ Crée automatiquement la base de données PostgreSQL
- ✅ Génère automatiquement la variable `DATABASE_URL`
- ✅ Connecte automatiquement la base au service web
- ✅ Injecte `DATABASE_URL` dans l'environnement

### 2. Le fichier `settings_prod.py`

Votre configuration Django lit automatiquement `DATABASE_URL` :

```python
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
```

**Django se connecte automatiquement** à PostgreSQL si `DATABASE_URL` existe !

---

## 📋 Étapes pour Connecter la BD

### Méthode 1 : Déploiement via `render.yaml` (AUTOMATIQUE) ✅

1. **Poussez votre code** sur GitHub (déjà fait)
2. **Dans Render Dashboard** :
   - Cliquez sur **"New +"** → **"Blueprint"**
   - Connectez votre repo GitHub
   - Render détectera automatiquement `render.yaml`
   - Cliquez sur **"Apply"**
3. **Render va automatiquement :**
   - Créer la base de données PostgreSQL
   - Créer le service web
   - Connecter la base au service
   - Déployer votre application

**C'est tout ! La connexion est automatique.** 🎉

---

### Méthode 2 : Création Manuelle

Si vous avez déjà créé le service web sans la base :

#### Étape 1 : Créer la Base de Données

1. Dans Render Dashboard, cliquez sur **"New +"**
2. Sélectionnez **"PostgreSQL"**
3. Configurez :
   - **Name** : `liftandlight-db`
   - **Database** : `liftandlight`
   - **User** : `liftandlight`
   - **Plan** : `Free`
4. Cliquez sur **"Create Database"**

#### Étape 2 : Connecter la Base au Service Web

**Méthode : Ajouter Manuellement `DATABASE_URL`** ✅

Le bouton "Link Database" n'est pas toujours visible dans Render. Voici la méthode manuelle qui fonctionne toujours :

1. **Allez sur votre base de données** `liftandlight-db` dans Render Dashboard
2. **Trouvez l'URL de connexion** :
   - Regardez dans l'onglet **"Info"** ou **"Connections"**
   - Cherchez **"Internal Database URL"** ou **"Connection String"**
   - L'URL ressemble à : `postgresql://user:password@hostname:port/database`
3. **Copiez cette URL complète**
4. **Allez sur votre service web** → **"Environment"** (ou **"Settings"** → **"Environment"**)
5. **Ajoutez une nouvelle variable** :
   - Cliquez sur **"Add Environment Variable"** ou **"Add Variable"**
   - **Key** : `DATABASE_URL` (en majuscules, exactement comme ça)
   - **Value** : Collez l'URL que vous avez copiée
6. **Cliquez sur "Save Changes"** ou **"Save"**
7. **Redéployez votre service** (Render le fera automatiquement ou cliquez sur "Manual Deploy")

**C'est tout !** Django utilisera maintenant PostgreSQL au lieu de SQLite. ✅

---

## ✅ Vérifier la Connexion

### 1. Vérifier dans les Logs

Après le déploiement, vérifiez les logs de votre service web :

```bash
# Dans Render Dashboard → Logs
# Vous devriez voir :
# "Operations to perform: Apply all migrations"
# "Running migrations..."
```

Si vous voyez des erreurs de connexion, vérifiez que `DATABASE_URL` est bien défini.

### 2. Vérifier dans le Shell Render

1. Allez sur votre service web
2. Cliquez sur **"Shell"**
3. Exécutez :
   ```bash
   python manage.py dbshell
   ```
4. Si ça fonctionne, vous verrez : `psql (PostgreSQL ...)`
5. Tapez `\q` pour quitter

### 3. Vérifier les Migrations

Dans le Shell Render :
```bash
python manage.py showmigrations
```

Tous les modèles devraient être marqués `[X]` (migrés).

---

## 🔧 Dépannage

### Problème : "django.db.utils.OperationalError: could not connect to server"

**Solutions :**
1. ✅ Vérifiez que `DATABASE_URL` existe dans Environment
2. ✅ Vérifiez que la base de données est **"Available"** (pas "Paused")
3. ✅ Vérifiez que vous utilisez `liftandlight.settings_prod` (pas `settings`)
4. ✅ Redéployez le service web

### Problème : "No such table: ..."

**Solution :**
```bash
# Dans le Shell Render
python manage.py migrate
```

### Problème : La base de données est "Paused"

**Solution :**
- Le plan Free de Render met en pause les bases inactives
- Cliquez sur **"Resume"** dans le dashboard de la base de données
- Attendez 1-2 minutes que la base redémarre

---

## 📝 Format de DATABASE_URL

Render génère automatiquement une URL au format :
```
postgresql://user:password@hostname:port/database
```

Exemple :
```
postgresql://liftandlight:abc123@dpg-xxxxx-a.oregon-postgres.render.com/liftandlight
```

**Vous n'avez pas besoin de la connaître**, `dj_database_url` la parse automatiquement !

---

## 🎉 Résumé

**Avec `render.yaml` :**
- ✅ Base créée automatiquement
- ✅ Connexion automatique
- ✅ `DATABASE_URL` injecté automatiquement
- ✅ Django se connecte automatiquement

**Vous n'avez rien à faire !** Render s'occupe de tout. 🚀

---

## 📚 Ressources

- [Documentation Render - Databases](https://render.com/docs/databases)
- [Documentation dj-database-url](https://github.com/jacobian/dj-database-url)

