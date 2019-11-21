"""Tests for fermion action models
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.linksmear.tests import UnsmearedTestCase
from lattedb.fermionaction.models import Hisq


class HisqTestCase(ObjectParser, TestCase):
    """Tests for Hisq fermion action.
    """
    # Default test
    model = Hisq
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.01",
        "quark_tag": "light",
        "naik": "1.23",
        "linksmear": UnsmearedTestCase.parameters,
    }
    consistency_check_changes = [{"quark_tag": "supermassive"}]

    # Additional tests
    def test_quark_tag_up(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "up"
        self.test_default_creation(parameters)

    def test_quark_tag_down(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "down"
        self.test_default_creation(parameters)

    def test_quark_tag_strange(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "strange"
        self.test_default_creation(parameters)

    def test_quark_tag_charm(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "charm"
        self.test_default_creation(parameters)

    def test_quark_tag_bottom(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "bottom"
        self.test_default_creation(parameters)

from lattedb.fermionaction.models import MobiusDW


class MobiusDWTestCase(ObjectParser, TestCase):
    """Tests for MobiusDW fermion action.
    """

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
    consistency_check_changes = [{"quark_tag": "supermassive"}]

    def test_quark_tag_up(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "up"
        self.test_default_creation(parameters)

    def test_quark_tag_down(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "down"
        self.test_default_creation(parameters)

    def test_quark_tag_strange(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "strange"
        self.test_default_creation(parameters)

    def test_quark_tag_charm(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "charm"
        self.test_default_creation(parameters)

    def test_quark_tag_bottom(self):
        parameters = dict(self.parameters)
        parameters["quark_tag"] = "bottom"
        self.test_default_creation(parameters)