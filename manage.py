#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        exc_msg = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        exc_info = (type(exc), exc, exc.__traceback__)
        raise ImportError(exc_msg).with_traceback(exc_info)

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
