import os
import sys
from pathlib import Path
from typing import Any

from decouple import config, Csv
import dj_database_url
from kombu import Queue

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_DIR = os.path.join(BASE_DIR)

sys.path.append(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-s=vv$ag-c%^i&qa=_wgz_+1vsfm58vj@4pq!#x$5k@77&$x3k-'
)


# SECURITY WARNING: don't run with debug turned on in production!
ENV = config('ENV', default='production')
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = []

ALLOW_DEV_APPS = config('ALLOW_DEV_APPS', default=False, cast=bool)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_celery_beat',
    'rest_framework',
]

LOCAL_APPS = [
    'picasso.apps.file',
]

INSTALLED_APPS += THIRD_PARTY_APPS
INSTALLED_APPS += LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'picasso.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'picasso.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = config('DATABASE_URL', default='postgres://postgres:postgres@db:5432/picasso')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600),
}


REDIS_URL = config('REDIS_URL', default='redis://redis:6379/0')

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# ------------------------------- FILE SYSTEM ---------------------------------
STATIC_URL = '/static/'

STATIC_ROOT = config('STATIC_ROOT')
if not STATIC_ROOT:
    STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = config('MEDIA_ROOT')
if not MEDIA_ROOT:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')

# --------------------------------- SECURITY ----------------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
USE_X_FORWARDED_HOST = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
ADDITIONAL_CSRF_TRUSTED_ORIGINS = config('ADDITIONAL_CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

hostname = config('BUSINESS_INTELLIGENCE_HOSTNAME', None) or config('HOST_IP_ADDRESS', default='http://127.0.0.1')
CSRF_TRUSTED_ORIGINS = [
    hostname,
    hostname + ':8010',
    *ADDITIONAL_CSRF_TRUSTED_ORIGINS,
]

# --------------------------------- LOGGING -----------------------------------
LOG_LEVEL = config('LOG_LEVEL', default='WARNING', cast=str).upper()
LOG_DIR = config('LOG_DIR', default=None)
LOG_FILE_SIZE = config('LOG_FILE_SIZE', default=4096, cast=int)

LOGGING: dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[{asctime}] {levelname:8} | {module:>10} @ {lineno:<5} | {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
        'propagate': True,
    },
    'celery.task': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
        'propagate': False,
    },
    'loggers': {
        'spnego': {'level': 'WARNING'},
        'asyncio': {'level': 'WARNING'},
        'django.server': {'handlers': ['console']},
        'django.utils.autoreload': {'level': 'WARNING'},
    },
}

if LOG_DIR:
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    LOGGING['root']['handlers'].append('file')
    LOGGING['handlers']['file'] = {
        'filename': log_dir / 'picasso.log',
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1024 * LOG_FILE_SIZE,
        'backupCount': 10,
        'formatter': 'default',
    }

# ---------------------------------- CELERY -----------------------------------
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TIMEZONE = TIME_ZONE
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_QUEUE = 'default'

CELERY_QUEUES = (Queue('default', routing_key='default'),)
CELERY_TASK_QUEUES = (Queue('default'),)

# ------------------------------ CUSTOM SETTINGS ------------------------------
PRODUCT_TITLE = 'Picasso'
PRODUCT_VERSION = config('PRODUCT_VERSION', default='dev version')

# ------------------------------- REST FRAMEWORK ------------------------------
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
