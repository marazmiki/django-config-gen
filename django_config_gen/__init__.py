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


VERSION = (0, 2, 0, 'alpha', 1)


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])

    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])

    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version

    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])

    return version


__version__ = get_version()