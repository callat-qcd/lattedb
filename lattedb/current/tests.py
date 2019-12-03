"""
Unittests for the current module
"""

from django.test import TestCase

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.current.models import Local


class LocalParser(ObjectParser):
    model = Local
    _tree = None
    _parameters = {
        "diracstruct": "gamma_5",
        "momentum": "0",
        "description": "pseudoscalar",
    }


class LocalTestCase(LocalParser, BaseTest, TestCase):
    ""


from lattedb.current.models import Local4D


class Local4DParser(ObjectParser, TestCase):
    model = Local4D
    _tree = None
    _parameters = {"diracstruct": "gamma_3*gamma_5", "description": "A3"}


class Local4DTestCase(Local4DParser, TestCase):
    ""
