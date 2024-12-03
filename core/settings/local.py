from .base import *
import os

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS  = [
    'http://localhost:5173',
    'http://localhost:8000',
    'http://*.tsifactur.com',
    'https://*.tsifactur.com',
    'http://*.tsi.pe',
    'https://*.tsi.pe',
]
 
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:8000',
    'http://*.tsi.pe/',
    'https://*.tsi.pe/',
]

DATABASES = {
    'default': env.db()
}

STATIC_ROOT = os.path.join (BASE_DIR / 'staticfiles')
STATICFILES_DIRS = (os.path.join (BASE_DIR / 'static'),)
STATIC_URL = '/static/'


MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_URL = "/media/"