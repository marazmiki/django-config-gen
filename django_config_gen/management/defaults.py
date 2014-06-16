# -*- coding: utf-8 -*-
#Copyright (C) 2010, 2011 Seán Hayes
#
#Licensed under a BSD 3-Clause License. See LICENSE file.

import __main__
import os
from django.conf import settings

PROJECT_ROOT = os.path.abspath(os.path.dirname(__main__.__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')

_config_dir = os.path.join(PROJECT_ROOT, 'config')
TEMPLATES_DIR = os.path.join(_config_dir, 'templates')
GENERATED_DIR = os.path.join(_config_dir, 'generated')

CONTEXT_PROCESSORS = []

#Error is thrown when running "./manage.py syncdb" for the first time and this app is installed.
HOST = 'localhost'

if 'django.contrib.sites' in settings.INSTALLED_APPS:
    try:
        from django.contrib.sites.models import Site
        HOST = Site.objects.get_current().domain.split(':')[0]
    except Site.DoesNotExist:
        from django.db import transaction
        # try/except to avoid "django.db.transaction.TransactionManagementError: This code isn't under transaction management"
        try:
            transaction.rollback()
        except:
            pass
