# coding: utf-8

from django.conf import settings

TEMPLATE_DIR = getattr(settings, 'CONFIG_GEN_TEMPLATE_DIR', '')
GENERATED_DIR = getattr(settings, 'CONFIG_GEN_TEMPLATE_DIR', '')
