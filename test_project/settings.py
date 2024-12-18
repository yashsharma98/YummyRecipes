"""
Django settings for test_project project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from lib2to3.pytree import Base
import os
from pathlib import Path
import dj_database_url
import os
import pdfkit


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-67u-yp=hkj)j^h-%r%@a*oab7zc17$m7qxicb&x2s$0h5e2z+=')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# When debug is set to false we need to serve static files (css, images) for ruuning locally from
# a server (currently we are using AWS S3, for that we need id & secret key)

# DEBUG = os.environ.get("DEBUG", "False").lower() == "true"


# ALLOWED_HOSTS = ['192.168.1.5','127.0.0.1','192.168.29.52','localhost']

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

ALLOWED_HOSTS = ['*']

APPEND_SLASH = True

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
CACHES = {
'default': {
'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
}
}

# Application definition

INSTALLED_APPS = [
    'testingapp.apps.TestingappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hitcount',
    'django_browser_reload',
    'rest_framework',
    'django.contrib.humanize',
    'wkhtmltopdf',
    'ckeditor',
    'chartjs',
    'anymail',
    'import_export',
    'django_htmx',
    'gtts',
    'storages',
    'notifications',
    'tinymce',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    'testingapp.middleware.TrailingSlashMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'testingapp.middleware.CheckPasswordMiddleware',
    'testingapp.middleware.ClearExistingUserFirstnameMiddleware',
]

# X_FRAME_OPTIONS = 'SAMEORIGIN'

# Open weather api
OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')

SPOONACULAR_API_KEY = os.environ.get('SPOONACULAR_API_KEY')

# Openai api
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

NUTRITION_API_KEY = os.environ.get('NUTRITION_API_KEY')

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Mailgun api 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '"Yummy Recipes" <yummyrecipes@django.com>'

ROOT_URLCONF = 'test_project.urls'

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

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
                'testingapp.context_processors.theme',
                'testingapp.context_processors.colortheme',
                'testingapp.context_processors.defaulttheme',
                'testingapp.context_processors.search_autocomplete_data',
                'testingapp.context_processors.message_notifications',
                'testingapp.context_processors.most_searched_recipes',
                'testingapp.context_processors.todays_date',
            ],

            'libraries':{
            'noti_date_filter': 'testingapp.templatetags.noti_date_filter',
            'read_time_pluralize': 'testingapp.templatetags.read_time_pluralize',
            }
        },
    },
]

WSGI_APPLICATION = 'test_project.wsgi.application'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'
CKEDITOR_IMAGE_BACKEND = "pillow"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

ENVIRONMENT = os.environ.get('ENVIRONMENT')

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }


else:
    # PosgreSQL

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'recipes',
            'USER': 'postgres',
            'PASSWORD': 'postgresql',
            'HOST': 'localhost', 
            'PORT': '',           
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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    # Add more languages as needed
]

USE_I18N = True  # Enable internationalization

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

IMPORT_EXPORT_USE_TRANSACTIONS = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

if not 'DATABASE_URL' in os.environ:
    MEDIA_URL = '/media/'



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'testingapp', 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    }
}


if 'DATABASE_URL' in os.environ:

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = 'us-east-2'

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/images/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


TINYMCE_DEFAULT_CONFIG = {
    # 'height': 500,
    # 'width': 1000,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'testingapp.backends.EmailBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'CLIENT_ID': os.environ.get('GOOGLE_CLIENT_ID'),
        'SECRET': os.environ.get('GOOGLE_SECRET_KEY'),
    }
}

LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_ADAPTER = 'testingapp.adapters.SocialAccountAdapter'