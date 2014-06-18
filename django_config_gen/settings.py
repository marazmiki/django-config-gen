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


def s(key, default=None):
    """
    Settings safe setter
    """
    return getattr(settings, key, default)

# Directory
TEMPLATES_DIR = s('CONFIG_GEN_TEMPLATES_DIR', None)


# Directory for generated files
GENERATED_DIR = s('CONFIG_GEN_GENERATED_DIR', None)


#
FILE_TEMPLATES = s('CONFIG_GEN_FILE_TEMPLATES', ())


# Built-in context processors
BUILTIN_CONTEXT_PROCESSORS = s(
    'CONFIG_GEN_DEFAULT_CONTEXT_PROCESSORS',
    (
        'django_config_gen.context_processors.default',
        'django_config_gen.context_processors.host',
    )
)


# Custom context processors
CUSTOM_CONTEXT_PROCESSORS = s('CONFIG_GEN_CONTEXT_PROCESSORS', ())


# Combine built-in and custom context processors
CONTEXT_PROCESSORS = tuple(list(BUILTIN_CONTEXT_PROCESSORS) +
                           list(CUSTOM_CONTEXT_PROCESSORS))