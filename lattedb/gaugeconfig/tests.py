"""
Unittests for the gaugeconfig module
"""

from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.gaugeconfig.models import Nf211
from lattedb.gaugeaction.tests import LuescherWeiszTestCase
from lattedb.fermionaction.tests import HisqTestCaseLight
from lattedb.fermionaction.tests import HisqTestCaseStrange
from lattedb.fermionaction.tests import HisqTestCaseCharm


class Nf211TestCaseHisq(ObjectParser, TestCase):
    """Tests creation of the Luescher-Weisz action.
    """

    model = Nf211
    tree = {
        "gaugeaction": "LuescherWeisz",
        "light": "Hisq",
        "strange": "Hisq",
        "charm": "Hisq",
        "light.linksmear": "Unsmeared",
        "strange.linksmear": "Unsmeared",
        "charm.linksmear": "Unsmeared",
    }
    parameters = {
        "short_tag": "a12m310",
        "stream": "a",
        "config": "1000",
        "gaugeaction": LuescherWeiszTestCase.parameters,
        "nx": "24",
        "ny": "24",
        "nz": "24",
        "nt": "64",
        "light": HisqTestCaseLight.parameters,
        "strange": HisqTestCaseStrange.parameters,
        "charm": HisqTestCaseCharm.parameters,
        "mpi": "310",
    }
    consistency_check_changes = [
        {"light.quark_tag": "strange"},
        {"light.quark_tag": "up"},
        {"strange.quark_tag": "charm"},
        {"charm.quark_tag": "light"},
    ]

class Nf211TestCaseHisqAlt(ObjectParser, TestCase):
    """Tests creation of the Luescher-Weisz action.
    """

    model = Nf211
    tree = {
        "gaugeaction": "LuescherWeisz",
        "light": "Hisq",
        "strange": "Hisq",
        "charm": "Hisq",
        "light.linksmear": "Unsmeared",
        "strange.linksmear": "Unsmeared",
        "charm.linksmear": "Unsmeared",
    }
    parameters = {
        "short_tag": "a12m310",
        "stream": "a",
        "config": "1005",
        "gaugeaction": LuescherWeiszTestCase.parameters,
        "nx": "24",
        "ny": "24",
        "nz": "24",
        "nt": "64",
        "light": HisqTestCaseLight.parameters,
        "strange": HisqTestCaseStrange.parameters,
        "charm": HisqTestCaseCharm.parameters,
        "mpi": "310",
    }
    consistency_check_changes = [
        {"light.quark_tag": "strange"},
        {"light.quark_tag": "up"},
        {"strange.quark_tag": "charm"},
        {"charm.quark_tag": "light"},
    ]