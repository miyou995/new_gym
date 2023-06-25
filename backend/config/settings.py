"""
Django settings for acm project.
Generated by 'django-admin startproject' using Django 4.0.3.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os 
from pathlib import Path
from django.contrib.messages import constants as messages
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m@qx+wsk0=4r0)_7=#b*#6)tn6_n#@hv=*tt#!_2rotvo*4byl'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'authentication.apps.AuthenticationConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'client.apps.ClientConfig',
    'assurance.apps.AssuranceConfig',
    'abonnement.apps.AbonnementConfig',
    'materiel.apps.MaterielConfig',
    'salle_activite.apps.SalleActiviteConfig',
    'creneau.apps.CreneauConfig',
    'presence.apps.PresenceConfig',
    'salle_sport.apps.SalleSportConfig',
    'planning.apps.PlanningConfig',
    'transaction.apps.TransactionConfig',
    
    #third party app
    'rest_framework',
    # 'rest_framework.authtoken',
    'debug_toolbar',
    'corsheaders',
    # 'drf_multiple_model',
    'import_export',
    # 'djoser',
    'django_filters',  
    'simple_history',
    # 'schema_graph',#SCHEMA
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    # 'rest_framework.authtoken',
    # 'rest_auth',
    # 'allauth', 
    # 'allauth.account', 
    # 'allauth.socialaccount', 
    # 'rest_auth.registration', 
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
         "rest_framework.authentication.SessionAuthentication",
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'TIME_FORMAT':  '%H:%M',
    'DATETIME_FORMAT': '%d %m %Y %H:%M', 
    # "DATE_INPUT_FORMATS": ["%d-%m-%Y"],
    # 'PAGE_SIZE': 20,
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',# third party
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', #DJango debug toolbar
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000"
# ]

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'config.urls'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / 'build'],
        'DIRS': [BASE_DIR / 'build'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LOGGING ={
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': BASE_DIR / "debug.log"
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

AUTH_USER_MODEL = 'authentication.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

# real port : 6379
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

from celery.schedules import crontab
from datetime import datetime
if DEBUG == True:
    CELERY_BEAT_SCHEDULE = {  
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_test_device_1', 
            'schedule': crontab(minute=0, hour=6), 
        },
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_test_device_2', 
            'schedule': crontab(minute=0, hour=6), 
        },
    }
else:
    pass
    """
    
    CELERY_BEAT_SCHEDULE = {  
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_2', 
            'schedule': crontab(minute=0, hour=6), 
        },
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_3', 
            'schedule': crontab(minute=0, hour=6), 
        },
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_4', 
            'schedule': crontab(minute=0, hour=6), 
        },
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_5', 
            'schedule': crontab(minute=0, hour=6), 
        },
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_6', 
            'schedule': crontab(minute=0, hour=6), 
        },
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_7', 
            'schedule': crontab(minute=0, hour=6), 
        },
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_8', 
            'schedule': crontab(minute=0, hour=6), 
        },
        'Task_one_schedule' : {   
            'task': 'salle_activite.tasks.start_linsten_9', 
            'schedule': crontab(minute=0, hour=6), 
        },
    }
"""








MEDIA_URL = "/media/" 

MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
### 
STATIC_URL = '/static/'
# STATICFILES_DIR = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / 'assets'
STATICFILES_DIRS = [
   BASE_DIR / 'build/static',

#    BASE_DIR,
]


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/' 
###

SITE_ID = 1


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
  
# USE_THOUSAND_SEPARATOR = True

try:
    from .local_settings import *
except ImportError:
    pass
