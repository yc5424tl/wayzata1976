"""
Django settings for wayzata76_django project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

import django_heroku
from django.contrib import messages
from django.urls import reverse_lazy

import dj_database_url
# import collectfast

from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if os.getenv('DEPLOYMENT') == 'DEV':
    import dotenv

    DJANGO_READ_DOT_ENV_FILE = True

    dotenv_file = os.path.join(BASE_DIR, 'wayzata76_django/.env')

    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)

    # EMAIL_BACKEND = (
    #     "django.core.mail.backends.console.EmailBackend"
    # )
    # EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    # EMAIL_FILE_PATH = str(BASE_DIR.joinpath("sent_emails"))
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'TRUE'


DATABASE_URL = os.environ.get('DATABASE_URL')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "TRUE"

ALLOWED_HOSTS = ["wayzata76.herokuapp.com", "wayzata76.com", 'localhost']

MESSAGE_LEVEL = message_constants.INFO

# Application definition

INSTALLED_APPS = [
    #"django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wayzata76_web.apps.Wayzata76WebConfig",
    "fontawesome-free",
    "widget_tweaks",
    "storages",
    "s3file",
    'djrichtextfield',
    "tinymce",
    "django_material_icons",
]

# if os.getenv('USE_S3') == "TRUE":


#     memcache_servers = os.environ['MEMCACHIER_SERVERS']
#     memcache_username = os.environ['MEMCACHIER_USERNAME']
#     memcache_password = os.environ['MEMCACHIER_PASSWORD']

#     CACHES = {
#         'default': {
#             'BACKEND': 'django_bmemcached.memcached.BMemcached',
#             'TIMEOUT': None,
#             'LOCATION': memcache_servers,
#             'OPTIONS': {
#                 'username': memcache_username,
#                 'password': memcache_password,
#                 'MAX_ENTRIES': 15000,
#             },
#         }
#     }

    # COLLECTFAST_CACHE = 'default'
    # COLLECTFAST_THREADS = 20








MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "s3file.middleware.S3FileMiddleware",
]

ROOT_URLCONF = "wayzata76_django.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wayzata76_web.context_processor.galleries",
                "accounts.context_processors.login_form",
            ],
        },
    },
]

WSGI_APPLICATION = "wayzata76_django.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)


if 'ENABLE_SERVER_SIDE_CURSORS' in os.environ:
    DISABLE_SERVER_SIDE_CURSORS = False


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'TIMEOUT': 86400
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

# TIME_ZONE = 'UTC'
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# TEMPLATE_LOADERS = (
# 'django.template.loaders.filesystem.Loader',
# 'django.template.loaders.app_directories.Loader',
# )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

PROJECT_DIR = os.path.dirname(__file__)

AUTH_USER_MODEL = "wayzata76_web.CustomUser"

LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = reverse_lazy("index")
LOGOUT_REDIRECT_URL = reverse_lazy("index")

if os.getenv('DEPLOYMENT') == 'PROD':
    EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    EMAIL_USE_TLS = os.getenv('USE_TLS') == 'TRUE'


if os.getenv("USE_S3") == "TRUE":

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_LOCATION = "static"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_DEFAULT_ACL = None
    STATIC_URL = "/static/"
    STATICFILES_STORAGE = "wayzata76_web.storage_backends.StaticStorage"
    DEFAULT_FILE_STORAGE = "wayzata76_web.storage_backends.PublicMediaStorage"
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "wayzata76_web/static")]
    COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"


else:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    DEFAULT_FILE_STORAGE = "wayzata76_web.storage_backends.PublicMediaStorage"
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# DJRICHTEXTFIELD_CONFIG = {
#     # 'js': ['//cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js'],
#     'js': ['//cdn.ckeditor.com/4.14.0/standard/ckeditor.js'],
#     # 'init_template': 'djrichtextfield/init/tinymce.js',
#     'init_template': 'djrichtextfield/init/ckeditor.js',
#     # 'settings': {  #TinyMCE
#     #     'menubar': False,
#     #     'plugins': 'link image',
#     #     'toolbar': 'bold italic | link-image | removeformat',
#     #     'width': 700
#     # }
#     'settings': {
#         'toolbar': [
#             {'items': ['Format', '-', 'Bold', 'Italic', '-', 'RemoveFormat']},
#             {'items': ['Link', 'Unlink', 'Image', 'Table']},
#             {'items': ['Source']}
#         ],
#         'format_tags': 'p;h1;h2;h3',
#         'width': 700
#     }
# }

# TINYMCE_CONFIG = {
#     'js': ['//cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js'],
#     'init_template': 'djrichtextfield/init/tinymce.js',
#     'settings': {
#         'menubar': False,
#         'plugins': 'link image table code',
#         'toolbar': 'formatselect | bold italic | removeformat |'
#                    ' link unlink image table | code',
#         'block_formats': 'Paragraph=p;Header 1=h1;Header 2=h2;Header 3=h3',
#         'width': 700
#     },
#     'profiles': {
#         'mini': {
#             'toolbar': 'bold italic | removeformat'
#         }
#     }
# }

# CKEDITOR_CONFIG = {
#     'js': ['//cdn.ckeditor.com/4.14.0/standard/ckeditor.js'],
#     'init_template': 'djrichtextfield/init/ckeditor.js',
#     'settings': {
#         'toolbar': [
#             {'items': ['Format', '-', 'Bold', 'Italic', '-', 'RemoveFormat']},
#             {'items': ['Link', 'Unlink', 'Image', 'Table']},
#             {'items': ['Source']}
#         ],
#         'format_tags': 'p;h1;h2;h3',
#         'width': 700,
#     },
#     'profiles': {
#         'mini': {
#             'toolbar': [
#                 {'items': ['Bold', 'Italic', '-', 'RemoveFormat']},
#             ]
#         }
#     },
#     'sanitizer': lambda value: 'foo' + value,
#     'sanitizer_profiles': {
#         'baz': lambda value: value + 'baz'
#     }
# }

# DJRICHTEXTFIELD_CONFIG = CKEDITOR_CONFIG

TINYMCE_JS_URL = os.path.join(STATIC_URL, "js/tinymce/tinymce.min.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_URL, "js/tinymce")
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "statusbar": False,

    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,code,help,wordcount",

    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment code",

    "cleanup_on_startup": True,

    "selector": "textarea",

    "contextmenu": "formats | link image",

    "custom_undo_redo_levels": 10,
}

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True


MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}
if "ON_HEROKU" in os.environ:
    django_heroku.settings(locals(), staticfiles=False)



