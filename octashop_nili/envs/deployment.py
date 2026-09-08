# filename: deployment.py

from .common import *
from decouple import config  # type: ignore

ALLOWED_HOSTS = ['niliteb.com', 'www.niliteb.com', '91.212.174.66']

CSRF_TRUSTED_ORIGINS = [
    'https://niliteb.com',
    'https://www.niliteb.com',
]


CORS_ALLOWED_ORIGINS = ['https://niliteb.com', 'https://www.niliteb.com']
CORS_ALLOW_CREDENTIALS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION":  "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config('REDIS_PASSWORD'),
        }
    }
}


INSTALLED_APPS = [
    'daphne',
    'drf_spectacular',
    # 'gunicorn',
] + INSTALLED_APPS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'HOST': 'db',
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'PORT': config('DB_PORT')
    }
}

BASE_URL = 'https://niliteb.com/'


# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#     }
# }



