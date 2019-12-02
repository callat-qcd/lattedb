"""
Unittests for the gaugeconfig module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.gaugeconfig.models import Nf211

from lattedb.gaugeaction.tests import LuescherWeiszParser
from lattedb.fermionaction.tests import HisqLightParser
from lattedb.fermionaction.tests import HisqStrangeParser
from lattedb.fermionaction.tests import HisqCharmParser


class Nf211TParser(ObjectParser):
    """Interface for quickly defining gaugeconfigs
    """

    model = Nf211
    _tree = {
        "gaugeaction": "LuescherWeisz",
        "light": "Hisq",
        "strange": "Hisq",
        "charm": "Hisq",
        "light.linksmear": "Unsmeared",
        "strange.linksmear": "Unsmeared",
        "charm.linksmear": "Unsmeared",
    }
    _parameters = {
        "short_tag": "a12m310",
        "stream": "a",
        "config": "1000",
        "gaugeaction": LuescherWeiszParser.get_parameters(),
        "nx": "24",
        "ny": "24",
        "nz": "24",
        "nt": "64",
        "light": HisqLightParser.get_parameters(),
        "strange": HisqStrangeParser.get_parameters(),
        "charm": HisqCharmParser.get_parameters(),
        "mpi": "310",
    }
    _consistency_check_changes = [
        {"light.quark_tag": "strange"},
        {"light.quark_tag": "up"},
        {"strange.quark_tag": "charm"},
        {"charm.quark_tag": "light"},
    ]


class Nf211TestCaseHisq(Nf211TParser, BaseTest, TestCase):
    """Tests creation of the Luescher-Weisz action.
    """
