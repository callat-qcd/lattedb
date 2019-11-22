"""Tests for fermion action models
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.linksmear.tests import UnsmearedTestCase
from lattedb.linksmear.tests import WilsonFlowTestCase
from lattedb.fermionaction.models import Hisq


class HisqTestCaseLight(ObjectParser, TestCase):
    model = Hisq
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.0102",
        "quark_tag": "light",
        "naik": "0",
        "linksmear": UnsmearedTestCase.parameters,
    }
    consistency_check_changes = [
        {"quark_tag": "supermassive"},
        {"quark_tag": "Light"},
        {"quark_tag": "   "},
        {"quark_tag": ""},
    ]

class HisqTestCaseLightWF(ObjectParser, TestCase):
    model = Hisq
    tree = {"linksmear": "WilsonFlow"}
    parameters = {
        "quark_mass": "0.0102",
        "quark_tag": "light",
        "naik": "0",
        "linksmear": WilsonFlowTestCase.parameters,
    }

class HisqTestCaseUp(ObjectParser, TestCase):
    model = Hisq
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.0102",
        "quark_tag": "up",
        "naik": "0",
        "linksmear": UnsmearedTestCase.parameters,
    }


class HisqTestCaseDown(ObjectParser, TestCase):
    model = Hisq
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.0102",
        "quark_tag": "down",
        "naik": "0",
        "linksmear": UnsmearedTestCase.parameters,
    }


class HisqTestCaseStrange(ObjectParser, TestCase):
    model = Hisq
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.0509",
        "quark_tag": "strange",
        "naik": "0",
        "linksmear": UnsmearedTestCase.parameters,
    }


class HisqTestCaseCharm(ObjectParser, TestCase):
    model = Hisq
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.635",
        "quark_tag": "charm",
        "naik": "-0.2308",
        "linksmear": UnsmearedTestCase.parameters,
    }


class HisqTestCaseBottom(ObjectParser, TestCase):
    model = Hisq
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "1.2",
        "quark_tag": "bottom",
        "naik": "-0.2308",
        "linksmear": UnsmearedTestCase.parameters,
    }


from lattedb.fermionaction.models import MobiusDW


class MobiusDWTestCaseLight(ObjectParser, TestCase):
    model = MobiusDW
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.01",
        "quark_tag": "light",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedTestCase.parameters,
    }
    consistency_check_changes = [
        {"quark_tag": "supermassive"},
        {"quark_tag": "Light"},
        {"quark_tag": "   "},
        {"quark_tag": ""},
    ]

class MobiusDWTestCaseLightWF(ObjectParser, TestCase):
    model = MobiusDW
    tree = {"linksmear": "WilsonFlow"}
    parameters = {
        "quark_mass": "0.01",
        "quark_tag": "light",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": WilsonFlowTestCase.parameters,
    }

class MobiusDWTestCaseUp(ObjectParser, TestCase):
    model = MobiusDW
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.01",
        "quark_tag": "up",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedTestCase.parameters,
    }

class MobiusDWTestCaseDown(ObjectParser, TestCase):
    model = MobiusDW
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.01",
        "quark_tag": "down",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedTestCase.parameters,
    }

class MobiusDWTestCaseStrange(ObjectParser, TestCase):
    model = MobiusDW
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.0693",
        "quark_tag": "strange",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedTestCase.parameters,
    }

class MobiusDWTestCaseCharm(ObjectParser, TestCase):
    model = MobiusDW
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.2",
        "quark_tag": "charm",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedTestCase.parameters,
    }

class MobiusDWTestCaseCharm(ObjectParser, TestCase):
    model = MobiusDW
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.4",
        "quark_tag": "bottom",
        "l5": "8",
        "m5": "1.2",
        "b5": "1.25",
        "c5": "0.25",
        "linksmear": UnsmearedTestCase.parameters,
    }