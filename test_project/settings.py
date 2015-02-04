import os
SECRET_KEY = 'FOO'
DEBUG = True
ROOT_URLCONF = 'urls'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, '..', 'var', 'data.sqlite'),
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'stored_email'
]

STATIC_URL = '/static/'

EMAIL_BACKEND = 'stored_email.backends.StoreSendEmailBackend'
STORED_EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Celery
BROKER_TRANSPORT = 'django'
BROKER_BACKEND = 'memory'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
# MEDIA_ROOT = os.path.join(unicode(tmpdir), 'media')
