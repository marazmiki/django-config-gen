# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import with_statement
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings as django_settings
from django.utils.module_loading import import_by_path
from django.utils import six
from django.template import Template, Context
from django_config_gen import settings
import os


def render_to_string(template_string, context):
    return Template(template_string).render(Context(context))


def get_context():
    kwargs = {}
    kwargs.update(**django_settings._wrapped.__dict__)
    kwargs.update(**django_settings._wrapped.__dict__['default_settings'].__dict__)
    kwargs = {k: v for k, v in kwargs.items() if k.isupper()}

    for context_processor in settings.CONTEXT_PROCESSORS:
        try:
            items = import_by_path(context_processor)()
            assert isinstance(items, dict)
        except ImproperlyConfigured:
            raise
        except AssertionError:
            raise ImproperlyConfigured('context processor must return dict')
        kwargs.update(**items)

    return kwargs


def generate():
    if settings.GENERATED_DIR is None:
        raise ImproperlyConfigured('The CONFIG_GEN_GENERATED_DIR is required')
    if settings.TEMPLATES_DIR is None:
        raise ImproperlyConfigured('The CONFIG_GEN_TEMPLATES_DIR is required')

    context = get_context()

    for root, dirs, files in os.walk(settings.TEMPLATES_DIR):
        for d in dirs:
            if d in settings.FILE_TEMPLATES:
                d = context.get(d) or d

            src = os.path.join(root, d)
            dst = src.replace(settings.TEMPLATES_DIR, settings.GENERATED_DIR)

            if not os.path.exists(dst):
                os.makedirs(dst)

        for f in files:
            if f in settings.FILE_TEMPLATES:
                f = context.get(f) or f
            src = os.path.join(root, f)
            dst = src.replace(settings.TEMPLATES_DIR, settings.GENERATED_DIR)

            dirname = os.path.dirname(src)

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            render_template(src, dst)


def render_template(source, target):
    with open(source, 'r') as fi, open(target, 'w') as fo:
        rendered = render_to_string(template_string=fi.read(),
                                    context=get_context())
        if not six.PY3:
            rendered = rendered.encode('utf-8')
        fo.write(rendered)


print_settings = get_context