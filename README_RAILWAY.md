# Guide de Déploiement Railway - Dépannage

## Si vous rencontrez des erreurs de build

### Erreur "pip: command not found"

Railway/Nixpacks devrait automatiquement installer pip avec Python. Si vous voyez cette erreur :

1. **Vérifiez que Railway utilise Nixpacks** (pas Dockerfile)
2. **Assurez-vous que `requirements.txt` existe** à la racine
3. **Vérifiez les logs complets** pour voir quelle dépendance échoue

### Erreur lors de l'installation des dépendances

Si une dépendance spécifique échoue (comme `psycopg2-binary`), essayez :

1. **Installer les dépendances système** (si Railway le permet)
2. **Utiliser une version spécifique** de la dépendance problématique
3. **Vérifier les logs** pour voir l'erreur exacte

### Configuration actuelle

- **Procfile** : Définit la commande de démarrage
- **railway.json** : Configuration Railway (optionnel)
- **requirements.txt** : Dépendances Python

### Railway détecte automatiquement

Railway/Nixpacks détecte automatiquement :
- ✅ Python (via `requirements.txt` ou `runtime.txt`)
- ✅ Django (via `manage.py`)
- ✅ Installe les dépendances (`pip install -r requirements.txt`)
- ✅ Exécute les migrations (si configuré)

### Ce qui n'est PAS automatique

- ❌ `collectstatic` - doit être ajouté manuellement
- ❌ Variables d'environnement - doivent être configurées dans le dashboard

### Solution : Ajouter collectstatic au démarrage

Si les fichiers statiques ne sont pas collectés automatiquement, modifiez le `Procfile` :

```
web: python manage.py collectstatic --noinput && python -m gunicorn liftandlight.wsgi --bind 0.0.0.0:$PORT
```

**Note** : Cela ralentit le démarrage. Mieux vaut l'exécuter pendant le build si possible.

### Alternative : Script de build

Créez un fichier `build.sh` et configurez Railway pour l'utiliser :

```bash
#!/bin/bash
set -e
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput || true
```

Puis dans Railway, configurez le "Build Command" : `bash build.sh`

