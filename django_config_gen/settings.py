# coding: utf-8

from django.conf import settings as s

# Directory
TEMPLATES_DIR = getattr(s, 'CONFIG_GEN_TEMPLATES_DIR', None)

# Directory for generated files
GENERATED_DIR = getattr(s, 'CONFIG_GEN_GENERATED_DIR', None)

# Built-in context processors
DEFAULT_CONTEXT_PROCESSORS = getattr(s, 'CONFIG_GEN_DEFAULT_CONTEXT_PROCESSORS', (
    'django_config_gen.context_processors.default',
    'django_config_gen.context_processors.host',
))

# Custom context processors
CONTEXT_PROCESSORS = getattr(s, 'CONFIG_GEN_CONTEXT_PROCESSORS', ())

#
FILE_TEMPLATES = getattr(s, 'CONFIG_GEN_FILE_TEMPLATES', ())
