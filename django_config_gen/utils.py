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
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings as django_settings
from django.utils.module_loading import import_by_path
from django.utils import six
from django.template import Template, Context
from django_config_gen import settings
import os
import logging


logger = logging.getLogger(__name__)


def render_to_string(template_string, context):
    """
    Render the template string with given context
    """
    return Template(template_string).render(Context(context))


def get_context():
    """
    Returns context for config generation
    """
    context = {}

    # Current project settings
    django_project_settings = django_settings._wrapped.__dict__

    # Built-in Django settings taken from django.conf.global_settings
    django_default_settings = django_project_settings['default_settings'].__dict__

    # Adds into context built-in settings
    context.update(**django_default_settings)

    # Override some of them with project settings
    context.update(**django_project_settings)

    # And cleans private attributes out
    context = {k: v for k, v in context.items() if k.isupper()}

    # Modify data with context processors
    for context_processor in settings.CONTEXT_PROCESSORS:
        try:
            items = import_by_path(context_processor)()
            assert isinstance(items, dict)
        except ImproperlyConfigured:
            raise
        except AssertionError:
            raise ImproperlyConfigured('context processor must return dict')
        context.update(**items)
    return context


def generate():
    """
    Generates configuration file based on templates
    """
    if settings.GENERATED_DIR is None:
        raise ImproperlyConfigured('The CONFIG_GEN_GENERATED_DIR is required')

    if settings.TEMPLATES_DIR is None:
        raise ImproperlyConfigured('The CONFIG_GEN_TEMPLATES_DIR is required')

    context = get_context()

    for root, dirs, files in os.walk(settings.TEMPLATES_DIR):
        for d in dirs:
            src = os.path.join(root, d)
            dst = src.replace(settings.TEMPLATES_DIR, settings.GENERATED_DIR)

            if d in settings.FILE_TEMPLATES:
                new2 = context.get(d, d)
                dst = dst.replace(d, context.get(d, d))
                #print('Wee! directory template [%s] [%s] > %s' % (d, new2, dst))

            if not os.path.exists(dst):
                os.makedirs(dst)

        for f in files:
            src = os.path.join(root, f)
            dst = src.replace(settings.TEMPLATES_DIR, settings.GENERATED_DIR)

            if f in settings.FILE_TEMPLATES:
                dst = dst.replace(f, context.get(f, f))

            dirname = os.path.dirname(src)

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            render_template(src, dst)


def render_template(source, target):
    """
    Renders template from `source` file name and saves rendered
    content into `target` file name
    """
    logger.debug('Rendering {source} to {target}'.format(source=source,
                                                         target=target))
    with open(source, 'r') as fi, open(target, 'w') as fo:
        rendered = render_to_string(template_string=fi.read(),
                                    context=get_context())
        if not six.PY3:                            # NOQA
            rendered = rendered.encode('utf-8')    # NOQA
        fo.write(rendered)


print_settings = get_context