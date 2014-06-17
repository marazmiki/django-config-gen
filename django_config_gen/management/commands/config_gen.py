# coding: utf-8
#
# Copyright (C) 2010-2014 Seán Hayes
# Copyrigjt (C) 2011-2014 Mikhail Porokhovnichenko
#
#

from django.core.management.base import NoArgsCommand
from django_config_gen.utils import generate


class Command(NoArgsCommand):
    help = ('Generates configuration files for apache, nginx, etc. '
            'using values in settings.py and the Django template system.')

    def handle_noargs(self, **options):
        generate()
