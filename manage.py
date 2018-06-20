#!/usr/bin/env python
import os
import sys
from subprocess import check_call, check_output, CalledProcessError

def customized_parameter(args):
    if len(args) >= 2:
        if args[1] == 'cleanup':
            check_call(['find', '.', '-name', '*.pyc', '-delete'])
            check_call(['find', '.', '-name', '*.xls', '-delete'])
            return True
        elif args[1] == 'startup':
            args.remove('startup')
            args.append('runserver')
            args.append('127.0.0.1:8080')
            return False
    return False

def main(args):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insights.settings")
    try:
        from django.core.management import execute_from_command_line
        if customized_parameter(args):
            return
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(args)

if __name__ == "__main__":
    main(sys.argv)
