"""
Django settings for djastebin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1^660lw28_jgsn(-30478w4^62eu5^_8&fw#&e#$lbk@a&_7&9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    ##### Default apps ######
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    ##### Project apps #####
    'apps.pastes',
    'apps.users',

    ##### Third party apps #####
    'django_cron',
    'widget_tweaks',
    'mptt',
    'password_reset',
    'social_auth',
    'notifications',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'djastebin.context_processors.recent_pastes',
    'social_auth.context_processors.social_auth_by_type_backends',

)

ROOT_URLCONF = 'djastebin.urls'

WSGI_APPLICATION = 'djastebin.wsgi.application'

# Social authentication
# http://django-social-auth.readthedocs.org/en/latest/

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

SOCIAL_AUTH_ENABLED_BACKENDS = ('facebook', 'google')

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

# Facebook app settings
FACEBOOK_APP_ID='1423882051196223'
FACEBOOK_API_SECRET='704b5ed4e7247b42384010205d7022ff'

FACEBOOK_EXTENDED_PERMISSIONS = ['email']

# Google app settings
GOOGLE_OAUTH2_CLIENT_ID = '645877344566-5eu9rb7do6dqen2fses7lv77tcovc9mh.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'IBGIuIZYTio-4oZyFJYd9wc1'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('pl', _('Polish')),
    ('en-us', _('English')),
)

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'conf/locale'),
)

# Url configuration

LOGIN_URL = '/login/'

LOGOUT_URL = '/logout/'

LOGIN_REDIRECT_URL = '/'

LOGIN_ERROR_URL = '/login/'

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATE_DIRS = (
     TEMPLATE_PATH,
)

CRON_CLASSES = (
    "apps.paste.cron.ClearExpiredPastesJob",
)

# Email configuration

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'djastebin'
EMAIL_HOST_PASSWORD = 'korwinkrul'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
