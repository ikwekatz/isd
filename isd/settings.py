import os
from pathlib import Path
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-g61=0%is74)anam&pya0@iqic-!&)u^q5yiw-nxzic6q4(kl33'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'jazzmin',
    'authentication',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'services',
    'activities',
    'office',
    'report',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'services.middleware.PermissionsPolicyMiddleware.PermissionsPolicyMiddleware',
]

ROOT_URLCONF = 'isd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'isd.wsgi.application'

db_url = config('DATABASE_URL')
db = dj_database_url.config(default=db_url, conn_max_age=600,conn_health_checks=True, ssl_require=False, )
DATABASES = {'default': db}
AUTH_USER_MODEL = 'authentication.CustomUser'

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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PERMISSIONS_POLICY = {
    "unload": []
}


JAZZMIN_SETTINGS  = {
    "site_title": "ISD",
    "site_header": "ICT Service Desk",
    "site_brand": "ICT Service Desk(ISD)",
    "site_logo": "logo.png",
    "login_logo":"logo.png",
    "site_logo_classes": "img-fluid img-thumbnail",
    "login_logo_classes": "img-fluid img-thumbnail",
    "welcome_sign": "Welcome to ICT Service Desk ",
    "copyright": "ICT Service Desk(ISD)",
    "show_version": False,
    "jazzmin_version":"0",
    "show_ui_builder":False,
}


