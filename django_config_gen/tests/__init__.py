# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.conf import settings
from django.core.management import call_command
import os
import tempfile
import shutil
import mock


class Test(test.TestCase):
    def setUp(self):
        self.root = os.path.dirname(__file__)
        self.input_dir = os.path.join(self.root, 'data')
        self.output_dir = os.path.join(tempfile.gettempdir(), 'config-gen')
        self.generated_dir = os.path.join(self.output_dir, 'generated')
        self.setUpDirectories()
        self._backup = {
            'GENERATED_DIR': getattr(settings, 'CONFIG_GEN_GENERATED_DIR', None),
            'TEMPLATES_DIR': getattr(settings, 'CONFIG_GEN_TEMPLATES_DIR', None),
        }
        settings.CONFIG_GEN_GENERATED_DIR = self.generated_dir
        settings.CONFIG_GEN_TEMPLATES_DIR = os.path.join(self.output_dir, 'data')

    def tearDown(self):
        shutil.rmtree(self.output_dir)
        for k, v in self._backup.items():
            setattr(settings, 'CONFIG_GEN_%s' % k, v)

    def setUpDirectories(self):
        for root, dirs, files in os.walk(self.input_dir):
            target_dir = root.replace(self.root, self.output_dir)
            if '.gitignore' in files:
                files.remove('.gitignore')
            for d in dirs:
                d = os.path.join(target_dir, d)
                if not os.path.exists(d):
                    os.makedirs(d)
            for f in files:
                src_file = os.path.join(root, f)
                dst_file = os.path.join(target_dir, f)
                with open(src_file, 'r') as src, open(dst_file, 'w') as dst:
                    dst.write(src.read())

    def assertFileExists(self, filename):
        self.assertTrue(os.path.exists(filename))

    def assertFileNotExists(self, filename):
        self.assertFalse(os.path.exists(filename))

    def assertGeneratedFileExists(self, filename):
        self.assertFileExists(os.path.join(self.generated_dir, filename))

    def assertGeneratedFileNotExists(self, filename):
        self.assertFileNotExists(os.path.join(self.generated_dir, filename))

    def test_tree(self):
        self.assertGeneratedFileNotExists('')
        call_command('config_gen')
        self.assertGeneratedFileExists('')

    def test_creates_empty_directories(self):
        self.assertGeneratedFileNotExists('')
        call_command('config_gen')
        self.assertGeneratedFileExists('')
        self.assertGeneratedFileExists('empty')
        self.assertGeneratedFileExists('full/empty_sub')

    def test_file_placeholders(self):
        with mock.patch('django_config_gen.utils') as p, \
            mock.patch('django.conf.settings') as p2:
            #self.settings(placeholder='Django')
            p.FILE_TEMPLATES = ['placeholder']
            call_command('config_gen')
            self.assertGeneratedFileExists('full/Django')

    def test_directory_placeholders(self):
        self.skipTest('todo')


class TestPrintFunctionCommand(test.TestCase):
    def test_1(self):
        call_command('print_settings')
