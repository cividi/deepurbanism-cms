"""Overwrite settings with production settings when going live."""
from .settings_base import *

import os
import logging.config

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()


# Basic configuration

# APP_NAME = env.get('APP_NAME', 'wagtailvue')

if 'SECRET_KEY' in env:
    SECRET_KEY = env['SECRET_KEY']

if 'ALLOWED_HOSTS' in env:
    ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')

if 'PRIMARY_HOST' in env:
    BASE_URL = 'http://%s/' % env['PRIMARY_HOST']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = env['SERVER_EMAIL']

if 'CACHE_PURGE_URL' in env:
    INSTALLED_APPS += ( 'wagtail.contrib.frontend_cache', )
    WAGTAILFRONTENDCACHE = {
        'default': {
            'BACKEND': 'wagtail.contrib.frontend_cache.backends.HTTPBackend',
            'LOCATION': env['CACHE_PURGE_URL'],
        },
    }


# Email via ESP

if 'MAILGUN_KEY' in os.environ:
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    ANYMAIL = {
        "MAILGUN_API_KEY": env['MAILGUN_KEY'],
        "MAILGUN_SENDER_DOMAIN": env['MAILGUN_DOMAIN']
    }
    DEFAULT_FROM_EMAIL = env['MAILGUN_FROM']

# Redis location can either be passed through with REDIS_HOST or REDIS_SOCKET

if 'REDIS_URL' in env:
    REDIS_LOCATION = env['REDIS_URL']
    BROKER_URL = env['REDIS_URL']

elif 'REDIS_HOST' in env:
    REDIS_LOCATION = env['REDIS_HOST']
    BROKER_URL = 'redis://%s' % env['REDIS_HOST']

elif 'REDIS_SOCKET' in env:
    REDIS_LOCATION = 'unix://%s' % env['REDIS_SOCKET']
    BROKER_URL = 'redis+socket://%s' % env['REDIS_SOCKET']

else:
    REDIS_LOCATION = None

if REDIS_LOCATION is not None:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_LOCATION,
            'KEY_PREFIX': APP_NAME,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

# Use Elasticsearch as the search backend for extra performance and better search results

if 'ELASTICSEARCH_URL' in env:
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.search.backends.elasticsearch5',
            'URLS': [env['ELASTICSEARCH_URL']],
            'INDEX': APP_NAME,
            'ATOMIC_REBUILD': True,
        },
    }

# Logging Configuration

# Clear prev config
LOGGING_CONFIG = None

# Get loglevel from env
LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console',],
        },
    },
})

try:
    from .local import *
except ImportError:
    pass
