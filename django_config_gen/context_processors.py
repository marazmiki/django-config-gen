# coding: utf-8

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import transaction
import os
import __main__


def default(*args, **kwargs):
    _project_root = os.path.abspath(os.path.dirname(__main__.__file__))
    _config_dir = os.path.join(_project_root, 'config')
    return {
        'PROJECT_ROOT': _project_root,
        'LOG_DIR': os.path.join(_project_root, 'logs'),
        'TEMPLATES_DIR': os.path.join(_config_dir, 'templates'),
        'GENERATED_DIR': os.path.join(_config_dir, 'generated'),
    }


def host(*args, **kwargs):
    _host = 'localhost'

    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        try:
            _host = Site.objects.get_current().domain.split(':')[0]
        except Site.DoesNotExist:
            # try/except to avoid "django.db.transaction.TransactionManagementError: This code isn't under transaction management"
            try:
                transaction.rollback()
            except transaction.TransactionManagementError:
                pass
    return {
        'HOST': _host
    }
