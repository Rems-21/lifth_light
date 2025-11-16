# 👤 Créer un Admin via Variables d'Environnement

## ✅ Solution Automatique

Vous pouvez créer un superutilisateur automatiquement au démarrage en définissant des variables d'environnement dans Render.

---

## 📋 Étapes dans Render

### 1. Ajouter les Variables d'Environnement

Dans le **Dashboard Render** :

1. Allez sur votre **Web Service**
2. Cliquez sur **"Environment"** (ou "Environment Variables")
3. Ajoutez ces 3 variables :

   ```
   ADMIN_USERNAME = admin
   ADMIN_EMAIL = admin@lifthlight.com
   ADMIN_PASSWORD = VotreMotDePasseSecurise123!
   ```

4. Cliquez sur **"Save Changes"**

### 2. Redéployer

Après avoir ajouté les variables, Render redéploiera automatiquement. Le superutilisateur sera créé automatiquement au démarrage.

---

## 🔧 Comment ça fonctionne

Le script `create_admin_from_env.py` :
- ✅ Vérifie si les variables `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` existent
- ✅ Crée le superutilisateur automatiquement si elles sont définies
- ✅ Ne fait rien si l'utilisateur existe déjà
- ✅ S'exécute à chaque démarrage (mais ne recrée pas l'utilisateur s'il existe)

Le script est appelé dans `start.sh` avant le démarrage de Gunicorn.

---

## 🔐 Sécurité

**⚠️ IMPORTANT :**

1. **Utilisez un mot de passe fort** pour `ADMIN_PASSWORD`
2. **Changez le mot de passe** après la première connexion si nécessaire
3. **Les variables d'environnement sont sécurisées** dans Render (non visibles publiquement)
4. **Vous pouvez supprimer les variables** après la création du premier admin

---

## 📝 Exemple de Configuration

Dans Render Dashboard → Environment :

```
ADMIN_USERNAME = admin
ADMIN_EMAIL = contact@lifthlight.com
ADMIN_PASSWORD = MonMotDePasseSuperSecurise2024!
```

Après le redéploiement, vous pourrez vous connecter à :
- URL : `https://votre-app.onrender.com/admin/`
- Username : `admin`
- Password : `MonMotDePasseSuperSecurise2024!`

---

## 🆘 Si ça ne fonctionne pas

1. **Vérifiez les logs** dans Render pour voir si le script s'exécute
2. **Vérifiez que les variables sont bien définies** dans Environment
3. **Vérifiez l'orthographe** : `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` (en majuscules)
4. **Redéployez manuellement** si nécessaire

---

## 🔄 Créer plusieurs admins

Le script ne crée qu'un seul admin. Pour créer plusieurs admins :

1. **Premier admin** : Via les variables d'environnement
2. **Autres admins** : Via l'interface admin Django ou le shell Render :
   ```bash
   python manage.py createsuperuser
   ```

---

## 💡 Alternative : Script personnalisé

Si vous voulez créer plusieurs admins ou personnaliser, vous pouvez modifier `projets/management/commands/create_admin_from_env.py`.

---

**C'est tout ! Plus besoin d'utiliser le Shell Render pour créer l'admin ! 🎉**

