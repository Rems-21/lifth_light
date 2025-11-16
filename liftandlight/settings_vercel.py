"""
Django settings for Vercel deployment
"""
from .settings import *
import os

# Override database settings for Vercel
# Use environment variable DATABASE_URL if available
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Parse PostgreSQL URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback: Use SQLite in memory (temporary, not persistent)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

# Disable migrations if database is not available
if DATABASE_URL is None:
    # This will cause issues, but at least the app won't crash on startup
    pass

# Static files - use WhiteNoise for Vercel
INSTALLED_APPS += ['whitenoise.runserver_nostatic']
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

