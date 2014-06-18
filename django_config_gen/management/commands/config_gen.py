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
from django.core.management.base import NoArgsCommand
from django_config_gen.utils import generate


class Command(NoArgsCommand):
    help = ('Generates configuration files for apache, nginx, etc. '
            'using values in settings.py and the Django template system.')

    def handle_noargs(self, **options):
        generate()