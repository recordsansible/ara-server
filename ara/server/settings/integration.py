from .base import *  # noqa

DEBUG = False

SECRET_KEY = 'INTEGRATION_SECRET_KEY'

# TODO: Currently required due to the usage of testclient in the offline client :(
ALLOWED_HOSTS = ('testserver',)
