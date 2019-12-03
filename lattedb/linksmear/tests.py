"""Unittests for the linksmear module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.linksmear.models import Unsmeared


class UnsmearedParser(ObjectParser):
    model = Unsmeared
    _tree = None
    _parameters = {}


class UnsmearedTestCase(UnsmearedParser, BaseTest, TestCase):
    """Tests creation of the Unsmeared link smear.
    """


from lattedb.linksmear.models import WilsonFlow


class WilsonFlowParser(ObjectParser):
    model = WilsonFlow
    _tree = None
    _parameters = {"flowtime": "1.0", "flowstep": "20"}


class WilsonFlowTestCase(WilsonFlowParser, BaseTest, TestCase):
    """Tests creation of Wilson Flow link smear
    """
