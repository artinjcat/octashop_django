from decouple import config
import os

from django.core.asgi import get_asgi_application





if config('DJANGO_DEVELOPMENT', default=False, cast=bool):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'octashop_nili.envs.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'octashop_nili.envs.deployment')




application = get_asgi_application()
