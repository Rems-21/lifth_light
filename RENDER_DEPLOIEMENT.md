# 🚀 Déploiement sur Render - Guide Étape par Étape

## ✅ Votre projet est déjà configuré !

Votre projet contient déjà `render.yaml` avec toute la configuration nécessaire. Il ne vous reste qu'à suivre ces étapes simples :

---

## 📋 ÉTAPES DE DÉPLOIEMENT (5 minutes)

### 1. Créer un compte Render

1. Allez sur **https://render.com**
2. Cliquez sur **"Get Started for Free"**
3. Connectez-vous avec votre compte **GitHub**
4. Autorisez Render à accéder à vos dépôts

### 2. Créer un nouveau Web Service

1. Dans le dashboard Render, cliquez sur **"New +"**
2. Sélectionnez **"Web Service"**
3. Connectez votre dépôt GitHub : **`Rems-21/lifth_light`**
4. Render détectera automatiquement le fichier `render.yaml` ✅

### 3. Vérifier la configuration

Render devrait automatiquement :
- ✅ Détecter Python
- ✅ Utiliser `render.yaml` pour la configuration
- ✅ Créer une base de données PostgreSQL
- ✅ Configurer les variables d'environnement

**Vérifiez que :**
- **Build Command** : `python -m pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Start Command** : `python -m gunicorn liftandlight.wsgi --bind 0.0.0.0:$PORT`
- **Environment** : `Python 3`

### 4. Variables d'environnement (automatiques)

Render configure automatiquement via `render.yaml` :
- ✅ `DJANGO_SETTINGS_MODULE=liftandlight.settings_prod`
- ✅ `SECRET_KEY` (généré automatiquement)
- ✅ `DATABASE_URL` (créé automatiquement avec la base de données)

**Vous pouvez aussi ajouter manuellement** (dans Settings → Environment) :
- `DEBUG=False` (pour la production)

### 5. Créer la base de données PostgreSQL

1. Dans le dashboard Render, cliquez sur **"New +"**
2. Sélectionnez **"PostgreSQL"**
3. Choisissez le plan **"Free"**
4. Nommez-la : `liftandlight-db`
5. Render créera automatiquement `DATABASE_URL`

**OU** : Render peut créer la base de données automatiquement via `render.yaml` ✅

### 6. Déployer !

1. Cliquez sur **"Create Web Service"**
2. Render va :
   - ✅ Installer les dépendances
   - ✅ Exécuter `collectstatic`
   - ✅ Exécuter les migrations (automatiquement)
   - ✅ Démarrer votre site

### 7. Créer le superutilisateur (AUTOMATIQUE)

**Option 1 : Via Variables d'Environnement (RECOMMANDÉ)** ✅

1. Dans le dashboard Render, allez sur votre service → **"Environment"**
2. Ajoutez ces variables :
   - `ADMIN_USERNAME` = `admin`
   - `ADMIN_EMAIL` = `admin@lifthlight.com`
   - `ADMIN_PASSWORD` = `VotreMotDePasseSecurise`
3. **Save Changes** - Render redéploiera automatiquement
4. Le superutilisateur sera créé automatiquement ! 🎉

**Option 2 : Via le Shell Render**

Si vous préférez créer manuellement :
```bash
python manage.py createsuperuser
```

**Voir** `ADMIN_ENV_VARIABLES.md` pour plus de détails.

---

## ✅ Vérification après déploiement

1. **Votre site devrait être accessible** à : `https://votre-app.onrender.com`
2. **Vérifiez les logs** dans le dashboard Render
3. **Testez les pages** :
   - Page d'accueil : `/`
   - Projets : `/projets/`
   - Blog : `/blog/`
   - Pages statiques : `/ascenceur/about.html`, etc.

---

## 🔧 Si vous rencontrez des problèmes

### Les styles ne s'affichent pas ?

1. Vérifiez les logs - `collectstatic` doit s'exécuter
2. Vérifiez que `DJANGO_SETTINGS_MODULE=liftandlight.settings_prod`
3. Vérifiez la console du navigateur (F12) pour les erreurs 404

### Erreur de base de données ?

1. Vérifiez que la base de données PostgreSQL est créée
2. Vérifiez que `DATABASE_URL` est bien configuré
3. Exécutez manuellement : `python manage.py migrate`

### Erreur lors du build ?

1. Vérifiez les logs de build complets
2. Assurez-vous que toutes les dépendances sont dans `requirements.txt`
3. Vérifiez que Python 3.10.9 est bien utilisé

---

## 📝 Configuration actuelle

Votre `render.yaml` configure :
- ✅ Build avec `collectstatic`
- ✅ Start avec Gunicorn
- ✅ Variables d'environnement
- ✅ Base de données PostgreSQL

**Tout est prêt !** Il ne vous reste qu'à déployer ! 🚀

---

## 🎯 Prochaines étapes après déploiement

1. **Créer un superutilisateur** :
   ```bash
   python manage.py createsuperuser
   ```

2. **Accéder à l'admin Django** :
   - URL : `https://votre-app.onrender.com/admin/`
   - Utilisez les identifiants du superutilisateur

3. **Ajouter des projets** via l'admin Django

4. **Ajouter des articles de blog** via l'admin Django

---

## 💡 Astuces

- **Plan gratuit Render** : Le site peut être "endormi" après 15 minutes d'inactivité (première requête sera lente)
- **Upgrade** : Pour éviter l'endormissement, upgrade vers le plan "Starter" ($7/mois)
- **Logs** : Toujours vérifier les logs en cas de problème
- **Variables d'environnement** : Modifiez-les dans Settings → Environment

---

**C'est tout ! Votre site sera en ligne en 5 minutes ! 🎉**

