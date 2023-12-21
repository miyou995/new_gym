from celery.schedules import crontab
from datetime import datetime


SECRET_KEY = 'QCqcqscrtgjczvgrezg0hzd6t%82b3ol#^)6(94^o+nto(5h#kg#f7z!yh8'
DEBUG = True

ALLOWED_HOSTS = ['*'] # a modifier apres l'integration du nom de domaine

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "octogym_db",
        'USER': "octopus",
        'PASSWORD': "miyou0209",
        'HOST': "localhost",
        'PORT': "5432",
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

# if DEBUG == True:
#     CELERY_BEAT_SCHEDULE = {  
#         'start_linsten_test_device_2': {
#             'task': 'salle_activite.tasks.start_linsten_test_device_2',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_linsten_test_device_1': {
#             'task': 'salle_activite.tasks.start_linsten_test_device_1',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#     }
# if DEBUG == False:
#     CELERY_BEAT_SCHEDULE = {
#         'start_linsten_2': {
#             'task': 'salle_activite.tasks.start_linsten_2',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_linsten_3': {
#             'task': 'salle_activite.tasks.start_linsten_3',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_linsten_4': {
#             'task': 'salle_activite.tasks.start_linsten_4',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_linsten_5': {
#             'task': 'salle_activite.tasks.start_linsten_5',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_linsten_6': {
#             'task': 'salle_activite.tasks.start_linsten_6',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_linsten_7': {
#             'task': 'salle_activite.tasks.start_linsten_7',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_linsten_8': {
#             'task': 'salle_activite.tasks.start_linsten_8',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_linsten_9': {
#             'task': 'salle_activite.tasks.start_linsten_9',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_face_door_right': {
#             'task': 'salle_activite.tasks.start_face_door_right',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },
#         'start_face_door_left': {
#             'task': 'salle_activite.tasks.start_face_door_left',
#             'schedule': crontab(hour=START_HOUR, minute=START_MINUTE),
#         },

# }