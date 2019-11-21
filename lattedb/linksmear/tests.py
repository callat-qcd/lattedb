"""Unittests for the linksmear module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.linksmear.models import Unsmeared

class UnsmearedTestCase(ObjectParser, TestCase):
    """Tests creation of the Unsmeared link smear.
    """

    model = Unsmeared
    tree = None
    parameters = {}

from lattedb.linksmear.models import WilsonFlow

class WilsonFlowTestCase(ObjectParser, TestCase):
    """Tests creation of Wilson Flow link smear
    """

    model = WilsonFlow
    tree = None
    parameters = {"flowtime": "1.0", "flowstep": "20"}

