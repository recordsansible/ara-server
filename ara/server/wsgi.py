import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ara.server.settings")
# https://github.com/rochacbruno/dynaconf/issues/89
from dynaconf.contrib import django_dynaconf

application = get_wsgi_application()
