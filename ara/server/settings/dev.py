from .base import *  # noqa

SECRET_KEY = 'DEVELOPMENT_SECRET_KEY'
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ORIGIN_ALLOW_ALL = True

# Django built-in server and npm development server
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8000',
    'localhost:3000',
)
