# coding: utf-8

from django import test
from django.core.management import call_command
import os
import tempfile
import shutil


class Test(test.TestCase):
    def setUp(self):
        self.root = os.path.dirname(__file__)
        self.input_dir = os.path.join(self.root, 'data')
        self.output_dir = os.path.join(tempfile.gettempdir(), 'config-gen')
        self.generated_dir = os.path.join(self.output_dir, 'generated')
        self.setUpDirectories()

    def tearDown(self):
        shutil.rmtree(self.output_dir)
        pass

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
#        print("assert %s exists" % filename)
        self.assertTrue(os.path.exists(filename))

    def assertFileNotExists(self, filename):
#        print("assert %s *NOT* exists" % filename)
        self.assertFalse(os.path.exists(filename))

    def test_tree(self):
#        print('  *** output = %s\n  *** input = %s\n' % (self.output_dir, self.input_dir))
        with self.settings(CONFIG_GEN_GENERATED_DIR=self.generated_dir,
                           CONFIG_GEN_TEMPLATES_DIR=os.path.join(self.output_dir, 'data')):
            self.assertFileNotExists(self.generated_dir)
            call_command('config_gen')
#            print(self.generated_dir)
            self.assertFileExists(self.generated_dir)

    def test_creates_empty_directories(self):
        self.skipTest('todo')

    def test_file_placeholders(self):
        self.skipTest('todo')

    def test_directory_placeholders(self):
        self.skipTest('todo')


class TestPrintFunctionCommand(test.TestCase):
    def test_1(self):
        call_command('print_settings')
