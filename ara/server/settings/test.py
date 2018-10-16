import logging

from .base import *  # noqa

# TODO: Why is this here?
logging.disable(logging.CRITICAL)

DEBUG = False

SECRET_KEY = 'TEST_SECRET_KEY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ALLOWED_HOSTS = ('testserver',)
