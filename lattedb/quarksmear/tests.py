"""Unittests for the quarksmear module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.quarksmear.models import Point


class PointParser(ObjectParser):
    model = Point
    _tree = None
    _parameters = {}


class PointTestCase(PointParser, BaseTest, TestCase):
    """Tests creation of the Unsmeared link smear.
    """


from lattedb.quarksmear.models import GaugeCovariantGaussian


class GaugeCovariantGaussianParser(ObjectParser):

    model = GaugeCovariantGaussian
    _tree = None
    _parameters = {"radius": "3.0", "step": "30"}


class GaugeCovariantGaussianTestCase(GaugeCovariantGaussianParser, BaseTest, TestCase):
    """Tests creation of Wilson Flow link smear
    """
