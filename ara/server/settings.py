import os
import sys
import yaml

# Ensure default base configuration/data directory exists
ARA_DIR = os.environ.get("ARA_DIR", os.path.expanduser('~/.ara'))
if not os.path.isdir(ARA_DIR):
    os.makedirs(ARA_DIR, mode=0o700)

DEFAULT_CONFIG = os.path.join(ARA_DIR, "default_config.yaml")
# Create default configuration file if it doesn't exist
if not os.path.exists(DEFAULT_CONFIG):
    CONFIG = {
        "TIME_ZONE": "UTC",
        "USE_TZ": True,
        "SECRET_KEY": "ara-is-awesome",
        "ALLOWED_HOSTS": ["127.0.0.1"],
        "CORS_ORIGIN_ALLOW_ALL": True,
        "CORS_ORIGIN_WHITELIST": ("127.0.0.1:8000", "localhost:3000"),
        "STATIC_URL": "/static/",
        "STATIC_ROOT": os.path.join(ARA_DIR, "www", "static"),
        "MEDIA_URL": "/media/",
        "MEDIA_ROOT": os.path.join(ARA_DIR, "www", "media"),
        "DATABASES": {
            "default": {
                "ENGINE": os.environ.get("ARA_DATABASE_ENGINE", 'django.db.backends.sqlite3'),
                "NAME": os.environ.get("ARA_DATABASE_NAME", os.path.join(ARA_DIR, 'ara.sqlite')),
                "USER": os.environ.get("ARA_DATABASE_USER", None),
                "PASSWORD": os.environ.get("ARA_DATABASE_PASSWORD", None),
                "HOST": os.environ.get("ARA_DATABASE_HOST", None),
                "PORT": os.environ.get("ARA_DATABASE_PORT", None),
            }
        },
        "DEBUG": True,
        "LOG_LEVEL": "INFO",
        "LOGGING": {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"normal": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"}},
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "normal",
                    "level": "INFO",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "ara": {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": 0
                }
            },
            "root": {
                "handlers": ["console"],
                "level": "DEBUG"
            },
        }
    }
    with open(DEFAULT_CONFIG, "w") as config_file:
        yaml.dump({"default": CONFIG}, config_file, default_flow_style=False)

if os.environ.get("ARA_SETTINGS") is None:
    os.environ["ARA_SETTINGS"] = DEFAULT_CONFIG

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dynaconf.contrib.django_settings")
os.environ.setdefault("SETTINGS_MODULE_FOR_DYNACONF", "ara.server.settings")

# Django's pre-flight checks requires SECRET_KEY to be set before initializing
# INSTALLED_APPS.
# This is overwritten as soon as dynaconf is loaded from INSTALLED_APPS.
SECRET_KEY = True

# Prefix for dynaconf env variables
GLOBAL_ENV_FOR_DYNACONF = "ARA"

# Path to ini, json, yaml or toml configuration file
ENVVAR_FOR_DYNACONF = "ARA_SETTINGS"

ADMINS = ()

INSTALLED_APPS = [
    "dynaconf.contrib.django_dynaconf",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "ara.api",
    "ara.server.apps.AraAdminConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ara.server.urls"
APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "ara.server.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}
