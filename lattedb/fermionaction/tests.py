# pylint: disable=too-many-ancestors, missing-docstring, empty-docstring
"""Tests for fermion action models
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.linksmear.tests import UnsmearedParser
from lattedb.linksmear.tests import WilsonFlowParser
from lattedb.fermionaction.models import Hisq


class HisqLightParser(ObjectParser):
    model = Hisq
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.0102",
        "quark_tag": "light",
        "naik": "0",
        "linksmear": UnsmearedParser.get_parameters(),
    }
    _consistency_check_changes = [
        {"quark_tag": "supermassive"},
        {"quark_tag": "Light"},
        {"quark_tag": "   "},
        {"quark_tag": ""},
    ]


class HisqLightTestCase(HisqLightParser, BaseTest, TestCase):
    """
    """


class HisqLightWFParser(ObjectParser):
    model = Hisq
    _tree = {"linksmear": "WilsonFlow"}
    _parameters = {
        "quark_mass": "0.0102",
        "quark_tag": "light",
        "naik": "0",
        "linksmear": WilsonFlowParser.get_parameters(),
    }


class HisqLightWFTestCase(HisqLightWFParser, BaseTest, TestCase):
    """
    """


class HisqUpParser(ObjectParser):
    model = Hisq
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.0102",
        "quark_tag": "up",
        "naik": "0",
        "linksmear": UnsmearedParser.get_parameters(),
    }


class HisqUpTestCase(HisqUpParser, BaseTest, TestCase):
    """
    """


class HisqDownParser(ObjectParser):
    model = Hisq
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.0102",
        "quark_tag": "down",
        "naik": "0",
        "linksmear": UnsmearedParser.get_parameters(),
    }


class HisqDownTestCase(HisqDownParser, BaseTest, TestCase):
    """
    """


class HisqStrangeParser(ObjectParser):
    model = Hisq
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.0509",
        "quark_tag": "strange",
        "naik": "0",
        "linksmear": UnsmearedParser.get_parameters(),
    }


class HisqStrangeTestCase(HisqStrangeParser, BaseTest, TestCase):
    ""


class HisqCharmParser(ObjectParser):
    model = Hisq
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.635",
        "quark_tag": "charm",
        "naik": "-0.2308",
        "linksmear": UnsmearedParser.get_parameters(),
    }


class HisqCharmTestCase(HisqCharmParser, BaseTest, TestCase):
    ""


class HisqBottomParser(ObjectParser):
    model = Hisq
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "1.2",
        "quark_tag": "bottom",
        "naik": "-0.2308",
        "linksmear": UnsmearedParser.get_parameters(),
    }


class HisqBottomTestCase(HisqBottomParser, BaseTest, TestCase):
    ""


from lattedb.fermionaction.models import MobiusDW


class MobiusDWTestCaseLight(ObjectParser, BaseTest, TestCase):
    model = MobiusDW
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.01",
        "quark_tag": "light",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedParser.get_parameters(),
    }
    consistency_check_changes = [
        {"quark_tag": "supermassive"},
        {"quark_tag": "Light"},
        {"quark_tag": "   "},
        {"quark_tag": ""},
    ]


class MobiusDWTestCaseLightWF(ObjectParser, BaseTest, TestCase):
    model = MobiusDW
    _tree = {"linksmear": "WilsonFlow"}
    _parameters = {
        "quark_mass": "0.01",
        "quark_tag": "light",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": WilsonFlowParser.get_parameters(),
    }


class MobiusDWTestCaseUp(ObjectParser, BaseTest, TestCase):
    model = MobiusDW
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.01",
        "quark_tag": "up",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedParser.get_parameters(),
    }


class MobiusDWTestCaseDown(ObjectParser, BaseTest, TestCase):
    model = MobiusDW
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.01",
        "quark_tag": "down",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedParser.get_parameters(),
    }


class MobiusDWTestCaseStrange(ObjectParser, BaseTest, TestCase):
    model = MobiusDW
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.0693",
        "quark_tag": "strange",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedParser.get_parameters(),
    }


class MobiusDWTestCaseCharm(ObjectParser, BaseTest, TestCase):
    model = MobiusDW
    _tree = {"linksmear": "Unsmeared"}
    _parameters = {
        "quark_mass": "0.2",
        "quark_tag": "charm",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedParser.get_parameters(),
    }
