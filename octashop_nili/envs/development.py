from .common import *
from decouple import config  # type: ignore



ALLOWED_HOSTS = ['*']


CORS_ALLOWED_ORIGINS = [
    "http://0.0.0.0",
    "http://127.0.0.1",
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://localhost:6379/1",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

INSTALLED_APPS = [
    'daphne',
    'drf_spectacular'
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




CORS_ALLOW_CREDENTIALS = True

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

