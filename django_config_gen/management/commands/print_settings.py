# coding: utf-8
# Copyright (C) 2010, 2011 Seán Hayes
#
#Licensed under a BSD 3-Clause License. See LICENSE file.

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.management.base import NoArgsCommand
from django_config_gen.utils import print_settings
import json
import logging


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


class Command(NoArgsCommand):
    help = 'Prints out settings serialized as JSON.'

    def handle_noargs(self, **options):
        #remove logging statements from output
        l = logging.getLogger('')
        for h in l.handlers:
            l.removeHandler(h)
        l.addHandler(NullHandler())
        print(json.dumps(print_settings(), indent=4, sort_keys=True))
