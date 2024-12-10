
from celery.schedules import crontab
from datetime import datetime

DEBUG=True
SECRET_KEY = 'QCqcqscrtgjczvgrezg0hzd6t%82b3ol#^)6(94^o+nto(5h#kg#f7z!yh8'

ALLOWED_HOSTS = ['*'] # a modifier apres l'integration du nom de domaine

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'gym_bd',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',  
#         'PORT': '5432', 
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': "octogym_db",
#         'USER': "postgres",
#         'PASSWORD': "postgres",
#         'HOST': "localhost",
#         'PORT': "5432",
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "gym_bd",
        'USER': "postgres",
        'PASSWORD': "postgres",
        'HOST': "localhost",
        'PORT': "5433",
    }
}


STOP_HOUR   = 4
STOP_MINUTE = 1

START_HOUR   = 4
START_MINUTE = 11

CELERY_BEAT_SCHEDULE = {  
    'start_linsten_test_device_2': {
        'task': 'salle_activite.tasks.start_linsten_test_device_2',
        'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
    },
    'start_linsten_test_device_1': {
        'task': 'salle_activite.tasks.start_linsten_test_device_1',
        'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
    },
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "gym_db",
        'USER': "postgres",
        'PASSWORD': "postgres",
        'HOST': "localhost",
        'PORT': "5432",
    }
}