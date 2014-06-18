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
from django_config_gen import settings as djcgs
import functools


class config_gen_settings(object):    # NOQA
    """
    Overrides the django-config-gen settings for test purposes
    """

    def __init__(self, **kwargs):
        self.options = kwargs

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def __call__(self, test_func):
        """
        Taken from the Django source code:
        https://github.com/django/django/blob/master/django/test/utils.py#L149
        """
        if isinstance(test_func, type):
            if not issubclass(test_func, test.SimpleTestCase):
                raise Exception(
                    "Only subclasses of Django SimpleTestCase can be decorated "
                    "with override_settings")
            original_pre_setup = test_func._pre_setup
            original_post_teardown = test_func._post_teardown

            def _pre_setup(innerself):
                self.enable()
                original_pre_setup(innerself)

            def _post_teardown(innerself):
                original_post_teardown(innerself)
                self.disable()
            test_func._pre_setup = _pre_setup
            test_func._post_teardown = _post_teardown
            return test_func
        else:
            @functools.wraps(test_func)
            def inner(*args, **kwargs):
                with self:
                    return test_func(*args, **kwargs)
        return inner

    def enable(self):
        self.orig_values = {}
        for key, new_value in self.options.items():
            self.orig_values[key] = getattr(djcgs, key, None)
            setattr(djcgs, key, new_value)

    def disable(self):
        for key, old_value in self.orig_values.items():
            setattr(djcgs, key, old_value)
        del self.orig_values

