# coding: utf-8
#
# Copyright (C) 2010-2014 Seán Hayes
# Copyright (C) 2011-2014 Mikhail Porokhovnichenko
#
# Licensed under a BSD 3-Clause License. See LICENSE file.
#

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import transaction
import os


def default(*args, **kwargs):    # NOQA
    """
    Adds PROJECT_ROOT, LOG_DIR, TEMPLATES_DIR, GENERATED_DIR
    variables into context
    """
    project_root = os.path.abspath(os.path.dirname(__import__('__main__').__file__))
    config_dir = os.path.join(project_root, 'config')

    return {
        'PROJECT_ROOT': project_root,
        'LOG_DIR': os.path.join(project_root, 'logs'),
        'TEMPLATES_DIR': os.path.join(config_dir, 'templates'),
        'GENERATED_DIR': os.path.join(config_dir, 'generated'),
    }


def host(*args, **kwargs):    # NOQA
    """
    Adds HOST variable into context
    """
    hostname = 'localhost'

    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        try:
            hostname = Site.objects.get_current().domain.split(':')[0]
        except Site.DoesNotExist:
            try:
                transaction.rollback()
            except transaction.TransactionManagementError:
                pass
    return {
        'HOST': hostname
    }