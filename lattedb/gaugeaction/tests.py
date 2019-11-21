"""Unittests for the gaugeaction module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.gaugeaction.models import LuescherWeisz


class LuescherWeiszTestCase(ObjectParser, TestCase):
    """Tests creation of the Luescher-Weisz action.
    """

    model = LuescherWeisz
    tree = None
    parameters = {
        "beta": "6.0",
        "a_fm": "0.12",
        "u0": "0.86372",
    }