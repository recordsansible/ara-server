import os

from envparse import env

from .base import *  # noqa

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=list, default=[])

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('DATABASE_NAME', default=os.path.join(BASE_DIR, 'db.sqlite3')),  # noqa: F405
        'USER': env('DATABASE_USER', default=None),
        'PASSWORD': env('DATABASE_PASSWORD', default=None),
        'HOST': env('DATABASE_HOST', default=None),
        'PORT': env('DATABASE_PORT', default=None),
    }
}
