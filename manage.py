#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config  # type: ignore


def main():
    """Run administrative tasks."""
    if config('DJANGO_DEVELOPMENT', default=False, cast=bool):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'octashop_nili.envs.development')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'octashop_nili.envs.deployment')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
