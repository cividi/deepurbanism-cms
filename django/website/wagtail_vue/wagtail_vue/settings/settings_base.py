"""Common settings and globals."""

import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path

from django.core.exceptions import ImproperlyConfigured

import dj_database_url

env = os.environ.copy()

# ======== PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
# ======== END PATH CONFIGURATION

if 'DJANGO_ALLOWED_HOSTS' in env:
    ALLOWED_HOSTS = env['DJANGO_ALLOWED_HOSTS'].split(',')

# ======== DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
# ======== END DEBUG CONFIGURATION


# ======== MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('backend', 'admin@yourwebsite.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# ======== END MANAGER CONFIGURATION


# ======== GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Zurich'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# ======== END GENERAL CONFIGURATION


# ======== MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
# ======== END MEDIA CONFIGURATION


# ======== STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# Moving static assets to DigitalOcean Spaces as per:
# https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django
if 'STATIC_ENDPOINT_URL' in env:
    AWS_ACCESS_KEY_ID = os.getenv('STATIC_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('STATIC_SECRET_KEY')

    AWS_STORAGE_BUCKET_NAME = os.getenv('STATIC_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.getenv('STATIC_ENDPOINT_URL')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    AWS_DEFAULT_ACL = 'public-read'

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, AWS_LOCATION)
    STATIC_ROOT = 'static/'
else:
    STATIC_ROOT = os.environ.get('DJANGO_STATIC_DIR',
                             '/var/services/django/static')
    STATIC_URL = '/static/'
# ======== END STATIC FILE CONFIGURATION


# ======== SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
if 'DJANGO_SECRET_KEY' in env:
    SECRET_KEY = env['DJANGO_SECRET_KEY']
# ======== END SECRET CONFIGURATION


# ======== FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS # noqa: E501
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
# ======== END FIXTURE CONFIGURATION


# ======== TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors # noqa: E501
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            normpath(join(SITE_ROOT, 'templates')),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'debug': DEBUG,
        },
    },
]
# ======== END TEMPLATE CONFIGURATION


# ======== MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)
# ======== END MIDDLEWARE CONFIGURATION


# ======== URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
# ======== END URL CONFIGURATION


# ======== APP CONFIGURATION
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',

    'adminactions',
    'django_extensions',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.api.v2',

    "wagtail.contrib.routable_page",

    "grapple",
    "graphene_django",
    "channels",

    'rest_framework',
    'modelcluster',
    'taggit',
    'corsheaders',

    'apps.pages',
    'storages',

    'wagtail_references',
)
# ======== END APP CONFIGURATION


# ======== LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'wagtail': {
            'handlers':     [],
            'level':        'WARNING',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'django.request': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'django.security': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
            'formatter':    'verbose',
        },
    },
}
# ======== END LOGGING CONFIGURATION


# ======== WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
ASGI_APPLICATION = 'wagtail_vue.routing.application'
# ======== END WSGI CONFIGURATION

# ======== WAGTAIL SITE CONFIGURATION
WAGTAIL_SITE_NAME = "Wagtail/Vue Website"
# ======== END WAGTAIL SITE CONFIGURATION

# ======== GRAPPLE CONFIGURATION
GRAPHENE = { "SCHEMA": "grapple.schema.schema" }
GRAPPLE = { "apps": {"pages": "" }}
# ======== END GRAPPLE CONFIGURATION

# Database

if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.config()}

# ======== ERROR MESSAGE FOR MISSING ENVIRONMENT VARIABLES
def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the %s environment variable' % var_name
        raise ImproperlyConfigured(error_msg)
# ======== END ERROR MESSAGE FOR MISSING ENVIRONMENT VARIABLES
