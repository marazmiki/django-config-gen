# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import with_statement
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings as djsettings
from django.template import Template, Context
from django_config_gen import settings
import os


class Generator(object):
    def __init__(self):
        if settings.GENERATED_DIR is None:
            raise ImproperlyConfigured(
                'The CONFIG_GEN_GENERATED_DIR is required'
            )
        if settings.TEMPLATES_DIR is None:
            raise ImproperlyConfigured(
                'The CONFIG_GEN_TEMPLATES_DIR is required'
            )
        self.source_dir = settings.TEMPLATES_DIR
        self.target_dir = settings.GENERATED_DIR

    def generate(self):
        context = self.get_context()
#        print('file templates=', settings.FILE_TEMPLATES)
        for root, dirs, files in os.walk(self.source_dir):
            for dirname in dirs:
#                print(dirname)
                if dirname in settings.FILE_TEMPLATES:
#                    print("!!!!!")
                    dirname = context.get(dirname) or dirname

                source = os.path.join(root, dirname)
                target = source.replace(self.source_dir, self.target_dir)

                if not os.path.exists(target):
                    os.makedirs(target)

            for filename in files:
                if filename in settings.FILE_TEMPLATES:
#                    print("!!!!!!!!!!")
                    filename = context.get(filename) or filename
#                    print("FILENAME =%s" % filename)
                source = os.path.join(root, filename)
                target = source.replace(self.source_dir, self.target_dir)

                dirname = os.path.dirname(source)

                if not os.path.exists(dirname):
                    os.makedirs(dirname)

#                print("generating %s -> %s" % (source, target))
                self.render_template(source, target)

    def get_context(self):
        keys = {}
        keys.update(**djsettings.__dict__)
        keys.pop('_deleted', None)
        return keys

    def render_template(self, source, target):
        with open(source, 'r') as fi, open(target, 'w') as fo:
            tpl = fi.read()
            ctx = self.get_context()
            fo.write(Template(tpl).render(Context(ctx)).encode('utf-8'))


generator = Generator()
generate = generator.generate
print_settings = generator.get_context
