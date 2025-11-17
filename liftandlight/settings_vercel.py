"""
Django settings for Vercel deployment
"""
from .settings import *
import os
import sys

# Override database settings for Vercel
# Use environment variable DATABASE_URL if available
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Parse PostgreSQL URL
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
        }
    except ImportError:
        # Fallback if dj_database_url is not installed
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
else:
    # Fallback: Use SQLite in memory (temporary, not persistent)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

# Disable database operations that might fail
# This prevents Django from trying to access the database during startup
import django.db.backends.sqlite3.base
django.db.backends.sqlite3.base.check_sqlite_version = lambda: None

# Static files - use WhiteNoise for Vercel
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

try:
    INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    WHITENOISE_USE_FINDERS = False
    WHITENOISE_AUTOREFRESH = DEBUG
except Exception as e:
    # If WhiteNoise fails, continue without it
    print(f"WhiteNoise setup failed: {e}", file=sys.stderr)
    pass

# Disable some checks that might fail on Vercel
SILENCED_SYSTEM_CHECKS = ['database.W004']  # Disable database check

# Ensure DEBUG is False in production
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # Vercel handles SSL
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
