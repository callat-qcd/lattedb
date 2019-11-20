"""Unittests for the linksmear module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.linksmear.models import Unsmeared


class UnsmearedTestCase(ObjectParser, TestCase):
    """Tests creation of the Unsmeared link smear.
    """

    model = Unsmeared
