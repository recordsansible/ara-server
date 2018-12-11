#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    from ara import server

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ara.server.settings")
    from dynaconf.contrib import django_dynaconf
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
