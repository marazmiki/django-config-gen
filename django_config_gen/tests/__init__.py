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
from django import test
from django.conf import settings
from django.core.management import call_command
from django.utils import six
from django_config_gen.tests.utils import config_gen_settings
import json
import sys
import os
import tempfile
import shutil
import mock


# Package root directory
PACKAGE_ROOT = os.path.dirname(__file__)

# Temporary directory where generated files will be created
WORKING_DIR = os.path.join(tempfile.gettempdir(), 'config-gen')

# Test templates from package
RAW_DATA_DIR = os.path.join(PACKAGE_ROOT, 'data')

# Directory for Prepared templates (generated for tests)
TEMPLATES_DIR = os.path.join(WORKING_DIR, 'data')

# Directory where generated test files will be created
GENERATED_DIR = os.path.join(WORKING_DIR, 'generated')


@config_gen_settings(TEMPLATES_DIR=TEMPLATES_DIR,  GENERATED_DIR=GENERATED_DIR)
class TestConfigGenCommand(test.TestCase):
    """
    Test for `config_gen` management command
    """

    def setUp(self):
        self.root = os.path.dirname(__file__)
        self.output_dir = os.path.join(tempfile.gettempdir(), 'config-gen')
        self.input_dir = os.path.join(self.root, 'data')
        self.setUpDirectories()

    def tearDown(self):
        shutil.rmtree(self.output_dir)
        pass

    def setUpDirectories(self):
        for root, dirs, files in os.walk(RAW_DATA_DIR):
            target_dir = root.replace(PACKAGE_ROOT, WORKING_DIR)
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
        self.assertTrue(os.path.exists(filename), 'Filename %s doesn\'t exists' % filename)

    def assertFileNotExists(self, filename):
        self.assertFalse(os.path.exists(filename), 'Filename %s exists' % filename)

    def assertGeneratedFileExists(self, filename):
        self.assertFileExists(os.path.join(GENERATED_DIR, filename))

    def assertGeneratedFileNotExists(self, filename):
        self.assertFileNotExists(os.path.join(GENERATED_DIR, filename))

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
        def se():
            return {
                'placeholder': 'Django',
            }

        with config_gen_settings(FILE_TEMPLATES=['placeholder']), \
             mock.patch('django_config_gen.utils.get_context', side_effect=se) as f:
            call_command('config_gen')
            self.assertGeneratedFileExists('full/Django')

    def test_directory_placeholders(self):
        def se():
            return {
                'full': 'DjangoProject',
            }

        with config_gen_settings(FILE_TEMPLATES=['full']), \
             mock.patch('django_config_gen.utils.get_context', side_effect=se):
            call_command('config_gen')
            self.assertGeneratedFileExists('DjangoProject')
            self.assertGeneratedFileNotExists('full')
            self.assertGeneratedFileExists('DjangoProject/full_sub')
            self.assertGeneratedFileNotExists('DjangoProject/DjangoProject_sub')


class TestPrintFunctionCommand(test.TestCase):
    """
    Test for `print_settings` management command
    """

    def setUp(self):
        """
        Avoid stdout writing
        """
        self.orig_stdout = sys.stdout
        sys.stdout = six.StringIO()

    def tearDown(self):
        """
        Take stdout back
        """
        sys.stdout = self.orig_stdout

    def test_smoke(self):
        """
        Smoke test -- e.g. command just works and not raises an exceptions
        """
        call_command('print_settings')

    def test_is_json(self):
        """
        Test that output is valid json with correct values
        """
        call_command('print_settings')

        # Move cursor into begin of buffer
        sys.stdout.seek(0)
        output = sys.stdout.read()

        # Whether `output` is a valid json? No exception expected
        data = json.loads(output)

        # Compare some values from project settings...
        self.assertEquals(settings.DEBUG, data['DEBUG'])