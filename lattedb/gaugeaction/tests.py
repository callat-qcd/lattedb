"""Unittests for the gaugeaction module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.gaugeaction.models import LuescherWeisz


class LuescherWeiszParser(ObjectParser):
    model = LuescherWeisz
    _tree = None
    _parameters = {
        "beta": "6.0",
        "a_fm": "0.12",
        "u0": "0.86372",
    }


class LuescherWeiszTestCase(LuescherWeiszParser, BaseTest, TestCase):
    """Tests creation of the Luescher-Weisz action.
    """
