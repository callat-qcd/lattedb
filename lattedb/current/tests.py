"""
Unittests for the current module
"""

from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.current.models import Local


class LocalTestCase(ObjectParser, TestCase):
    model = Local
    tree = None
    parameters = {
        "diracstruct": "gamma_5",
        "momentum": "0",
        "description": "pseudoscalar",
    }


from lattedb.current.models import Local4D


class Local4DTestCase(ObjectParser, TestCase):
    model = Local4D
    tree = None
    parameters = {"diracstruct": "gamma_3*gamma_5", "description": "A3"}
