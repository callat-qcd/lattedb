"""
Unittests for the propagator module
"""

from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.propagator.models import OneToAll

class OneToAllTestCase(ObjectParser, TestCase):
    model = OneToAll