# Structure du Projet Lift and Light

## Organisation des fichiers

```
dac/
├── manage.py                 # Script de gestion Django
├── requirements.txt          # Dépendances Python
├── db.sqlite3               # Base de données SQLite (généré)
├── README_DJANGO.md         # Documentation Django
├── STRUCTURE_PROJET.md      # Ce fichier
├── init_db.bat              # Script d'initialisation Windows
├── init_db.sh               # Script d'initialisation Linux/Mac
│
├── liftandlight/            # Configuration du projet Django
│   ├── __init__.py
│   ├── settings.py          # Paramètres Django
│   ├── urls.py              # URLs principales
│   ├── wsgi.py              # Configuration WSGI
│   └── asgi.py              # Configuration ASGI
│
├── projets/                 # Application Django "projets"
│   ├── __init__.py
│   ├── models.py            # Modèles Projet et ImageProjet
│   ├── admin.py             # Configuration admin Django
│   ├── views.py             # Vues (accueil, liste, détail)
│   ├── urls.py              # URLs de l'application
│   └── apps.py              # Configuration de l'app
│
├── templates/               # Templates Django
│   ├── base.html            # Template de base
│   └── projets/
│       ├── liste_projets.html
│       └── projet_detail.html
│
├── ascenceur/               # Fichiers statiques (HTML, CSS, JS, images)
│   ├── index.html           # Page d'accueil
│   ├── about.html
│   ├── contact.html
│   ├── services.html
│   ├── ascenseurs.html
│   ├── climatisation.html
│   ├── electricite.html
│   ├── groupes-electrogenes.html
│   ├── projets.html         # (Ancien, remplacé par Django)
│   │
│   ├── css/                  # Fichiers CSS
│   │   ├── bootstrap.min.css
│   │   ├── bootstrap-icons.css
│   │   └── styles.css
│   │
│   ├── js/                   # Fichiers JavaScript
│   │   ├── jquery.min.js
│   │   ├── bootstrap.min.js
│   │   ├── custom.js
│   │   ├── click-scroll.js
│   │   └── navbar-scroll.js
│   │
│   ├── images/               # Images statiques
│   │   ├── logo.jpg
│   │   ├── ascenceur.jpg
│   │   ├── climatisation.jpg
│   │   ├── electricite.jpg
│   │   ├── groupe_electrogene.jpg
│   │   └── ...
│   │
│   └── video/                # Vidéos
│       └── acceuil.mp4
│
├── media/                    # Fichiers uploadés (généré)
│   └── projets/              # Images uploadées via admin
│       ├── galeries/
│       └── ...
│
└── staticfiles/              # Fichiers statiques collectés (généré)
```

## URLs du projet

- `/` → Page d'accueil (index.html)
- `/projets/` → Liste des projets (Django)
- `/projets/<slug>/` → Détail d'un projet avec galerie (Django)
- `/admin/` → Administration Django
- `/ascenceur/about.html` → Page À propos
- `/ascenceur/contact.html` → Page Contact
- `/ascenceur/services.html` → Page Services
- `/ascenceur/ascenseurs.html` → Page Ascenseurs
- `/ascenceur/climatisation.html` → Page Climatisation
- `/ascenceur/electricite.html` → Page Électricité
- `/ascenceur/groupes-electrogenes.html` → Page Groupes Électrogènes

## Initialisation

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Initialiser la base de données

**Windows:**
```bash
init_db.bat
```

**Linux/Mac:**
```bash
chmod +x init_db.sh
./init_db.sh
```

**Ou manuellement:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 4. Lancer le serveur
```bash
python manage.py runserver
```

## Utilisation

1. Accéder à l'admin: `http://127.0.0.1:8000/admin/`
2. Se connecter avec le superutilisateur
3. Ajouter des projets dans "Projets" > "Projets"
4. Ajouter des images dans "Projets" > "Images" ou directement dans un projet

## Notes importantes

- Les fichiers statiques sont dans `ascenceur/`
- Les fichiers uploadés (images de projets) sont dans `media/projets/`
- La base de données SQLite est dans `db.sqlite3`
- Les templates Django sont dans `templates/`

