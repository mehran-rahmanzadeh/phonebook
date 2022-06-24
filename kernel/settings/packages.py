import os
from datetime import timedelta

from decouple import config
from django.conf import settings

from .base import (
    INSTALLED_APPS, MIDDLEWARE,
    STATIC_ROOT, BASE_DIR, STATICFILES_DIRS
)

# ############## #
#   EXTENSIONS   #
# ############## #

# admin
INSTALLED_APPS.append('django.contrib.admindocs')
INSTALLED_APPS.append('django.contrib.sites')

# packages
INSTALLED_APPS.append('rest_framework')
INSTALLED_APPS.append('corsheaders')
INSTALLED_APPS.append('django_filters')
INSTALLED_APPS.append('admin_footer')
INSTALLED_APPS.append('admin_honeypot')
INSTALLED_APPS.append('cachalot')
INSTALLED_APPS.append('drf_yasg')
INSTALLED_APPS.append('django_celery_beat')
INSTALLED_APPS.append('djcelery_email')

# Log

# Security

# Applications
INSTALLED_APPS.append('authentication')
INSTALLED_APPS.append('accounts')
INSTALLED_APPS.append('contacts')

# ###################### #
#     REST FRAMEWORK     #
# ###################### #

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',  # TODO: Should be removed in production
    ),
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '30/minute'
    # },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'RS512',
    'SIGNING_KEY': open(os.path.join(BASE_DIR, 'jwt-key')).read(),
    'VERIFYING_KEY': open(os.path.join(BASE_DIR, 'jwt-key.pub')).read(),
    'AUDIENCE': 'owner',
    'ISSUER': 'phonebook.com',

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'username',
    'USER_ID_CLAIM': 'identity',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# #################### #
#   BACKGROUND TASKS   #
# #################### #
BACKGROUND_TASK_RUN_ASYNC = True

# ########### #
#   CELERY    #
# ########### #
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'

# ########## #
#   CACHE    #
# ########## #
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_HOST')
    }
}
CACHE_TIMEOUT = 3600

# ########### #
#   UPLOAD    #
# ########### #
# FILE_UPLOAD_HANDLERS = [
#     'painless.utils.handlers.upload.ChunkFileUploadHandler'
# ]
# UPLOAD_CHUNK_SIZE = 2500 * 2 ** 10  # 2500 KB

# ######################### #
#       AdminInterface      #
# ######################### #
from datetime import datetime

ADMIN_FOOTER_DATA = {
    'site_url': 'https://phonebook.com',
    'site_name': 'Phonebook',
    'period': '{}'.format(datetime.now().year),
    'version': 'v0.0.1 - development'
}

# #################### #
# IMPORTANT VARIABLES  #
# #################### #
AUTH_USER_MODEL = 'accounts.CustomUser'

# ########################### #
#     DJANGO CORS HEADERS     #
# ########################### #
from corsheaders.defaults import default_headers
from corsheaders.defaults import default_methods

CORS_ALLOW_HEADERS = list(default_headers)
CORS_ALLOW_METHODS = list(default_methods)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True  # TODO: should be changed in production

CACHALOT_UNCACHABLE_APPS = ('admin', 'auth', 'calls')

OTP_TOKEN_EXPIRE_TIME = 120
OTP_REDIS_HOST = config('OTP_REDIS_HOST')
OTP_REDIS_PORT = config('OTP_REDIS_PORT')
OTP_REDIS_NAME = config('OTP_REDIS_NAME')

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
