"""Tests for fermion action models
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.linksmear.tests import UnsmearedTestCase
from lattedb.fermionaction.models import Hisq as HisqFermionAction


class HisqTestCase(ObjectParser, TestCase):
    """Tests for Hisq fermion action.
    """

    model = HisqFermionAction
    tree = {"linksmear": "Unsmeared"}
    parameters = {
        "quark_mass": "0.01",
        "quark_tag": "light",
        "naik": "1.23",
        "linksmear": UnsmearedTestCase.parameters,
    }
    consistency_check_changes = [{"quark_tag": "not-light"}]
