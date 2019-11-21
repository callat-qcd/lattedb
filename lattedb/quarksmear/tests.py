"""Unittests for the quarksmear module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.quarksmear.models import Point

class PointTestCase(ObjectParser, TestCase):
    """Tests creation of the Unsmeared link smear.
    """

    model = Point
    tree = None
    parameters = {}

from lattedb.quarksmear.models import GaugeCovariantGaussian

class GaugeCovariantGaussianTestCase(ObjectParser, TestCase):
    """Tests creation of Wilson Flow link smear
    """

    model = GaugeCovariantGaussian
    tree = None
    parameters = {"radius": "3.0", "step": "30"}

