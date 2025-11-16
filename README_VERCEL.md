# Déploiement sur Vercel

Ce projet Django peut être déployé sur Vercel, mais il y a quelques limitations importantes à noter :

## Limitations de Vercel avec Django

1. **Base de données** : Vercel ne supporte pas SQLite en production. Vous devrez utiliser une base de données externe (PostgreSQL, MySQL, etc.) via des services comme :
   - [Supabase](https://supabase.com) (PostgreSQL gratuit)
   - [PlanetScale](https://planetscale.com) (MySQL)
   - [Railway](https://railway.app) (PostgreSQL)

2. **Fichiers statiques** : Les fichiers statiques doivent être servis via un CDN ou configurés dans `vercel.json`. Pour la production, utilisez `whitenoise` ou servez les fichiers statiques via un CDN.

3. **Fichiers média** : Les fichiers uploadés ne peuvent pas être stockés localement sur Vercel. Utilisez un service de stockage cloud comme :
   - [Cloudinary](https://cloudinary.com)
   - [AWS S3](https://aws.amazon.com/s3/)
   - [Cloudflare R2](https://www.cloudflare.com/products/r2/)

## Configuration requise

1. **Variables d'environnement** : Configurez dans le dashboard Vercel :
   - `DJANGO_SETTINGS_MODULE=liftandlight.settings`
   - `SECRET_KEY` (générez une nouvelle clé secrète pour la production)
   - `DATABASE_URL` (si vous utilisez une base de données externe)
   - `ALLOWED_HOSTS` (ajoutez votre domaine Vercel)

2. **Collectstatic** : Avant le déploiement, exécutez :
   ```bash
   python manage.py collectstatic --noinput
   ```

## Alternatives recommandées

Pour un déploiement Django complet, considérez ces alternatives :

- **[Railway](https://railway.app)** : Support Django natif, base de données PostgreSQL incluse
- **[Render](https://render.com)** : Support Django, base de données PostgreSQL incluse
- **[Heroku](https://www.heroku.com)** : Support Django classique (payant)
- **[DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)** : Support Django

## Déploiement sur Vercel

1. Connectez votre dépôt GitHub à Vercel
2. Vercel détectera automatiquement le fichier `vercel.json`
3. Configurez les variables d'environnement dans le dashboard Vercel
4. Déployez !

## Notes importantes

- Le fichier `db.sqlite3` ne sera pas disponible sur Vercel
- Vous devrez migrer votre base de données vers un service externe
- Les fichiers média doivent être stockés sur un service cloud
- Pour la production, activez `DEBUG = False` dans `settings.py`

