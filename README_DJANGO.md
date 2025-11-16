# Backend Django - Gestion des Projets Lift and Light

## ⚠️ IMPORTANT - Initialisation requise

**Avant d'utiliser le site, vous DEVEZ initialiser la base de données !**

### Méthode rapide (Windows)
Double-cliquez sur `init_db.bat` ou exécutez :
```bash
init_db.bat
```

### Méthode rapide (Linux/Mac)
```bash
chmod +x init_db.sh
./init_db.sh
```

### Méthode manuelle
```bash
python manage.py makemigrations
python manage.py migrate
```

## Installation complète

1. **Installer les dépendances Python :**
```bash
pip install -r requirements.txt
```

2. **Initialiser la base de données** (voir ci-dessus)

3. **Créer un superutilisateur pour accéder à l'admin :**
```bash
python manage.py createsuperuser
```

4. **Lancer le serveur de développement :**
```bash
python manage.py runserver
```

5. **Accéder au site :**
- Site web: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Utilisation

### Accès à l'administration Django

1. Allez sur `http://127.0.0.1:8000/admin/`
2. Connectez-vous avec le superutilisateur créé
3. Vous pouvez maintenant :
   - Ajouter des projets
   - Ajouter des images à chaque projet
   - Gérer les catégories (Ascenseur, Climatisation, Électricité, Groupe Électrogène)

### Ajouter un projet

1. Dans l'admin Django, allez dans "Projets" > "Projets"
2. Cliquez sur "Ajouter un projet"
3. Remplissez :
   - **Titre** : Le nom du projet
   - **Description** : Description détaillée
   - **Catégorie** : Choisissez parmi les catégories disponibles
   - **Image principale** : Image de couverture (optionnel)
   - **Slug** : Généré automatiquement à partir du titre
   - **Actif** : Cochez pour afficher le projet sur le site

### Ajouter des images à un projet

1. Lors de la création/modification d'un projet, vous pouvez ajouter des images dans la section "Images"
2. Ou allez dans "Projets" > "Images" pour ajouter des images séparément
3. Pour chaque image :
   - **Projet** : Sélectionnez le projet
   - **Image** : Uploadez l'image
   - **Titre** : Titre optionnel pour l'image
   - **Ordre** : Ordre d'affichage (0, 1, 2, etc.)

## URLs

- **Liste des projets** : `http://127.0.0.1:8000/projets/`
- **Détail d'un projet** : `http://127.0.0.1:8000/projets/<slug-du-projet>/`
- **Admin** : `http://127.0.0.1:8000/admin/`

## Structure

- `projets/models.py` : Modèles Projet et ImageProjet
- `projets/admin.py` : Configuration de l'admin Django
- `projets/views.py` : Vues pour afficher les projets
- `projets/urls.py` : URLs de l'application
- `templates/projets/` : Templates HTML pour les projets

## Notes

- Les images sont stockées dans `media/projets/` et `media/projets/galeries/`
- Les images existantes dans `ascenceur/images/` peuvent être utilisées comme images principales
- Le système génère automatiquement un slug à partir du titre du projet

