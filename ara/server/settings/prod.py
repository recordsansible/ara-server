import os

from envparse import env

from .base import *  # noqa


SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=list, default=[])

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('DATABASE_NAME', default=os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': env('DATABASE_USER', default=None),
        'PASSWORD': env('DATABASE_PASSWORD', default=None),
        'HOST': env('DATABASE_HOST', default=None),
        'PORT': env('DATABASE_PORT', default=None),
    }
}

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'gvincent@redhat.com')
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = env.int('EMAIL_PORT', default=25)
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '[Ara] ')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=False)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
