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
