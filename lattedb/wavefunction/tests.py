"""Unittests for the quarksmear module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.wavefunction.models import Hadron4D


class Hadron4DParser(ObjectParser):
    model = Hadron4D
    _tree = None
    _parameters = {
        "description": "iddqd",
        "strangeness": "0",
        "irrep": "G1",
        "embedding": "1",
        "parity": "1",
        "spin_x2": "1",
        "spin_z_x2": "1",
        "isospin_x2": "1",
        "isospin_z_x2": "1",
    }
    _consistency_check_changes = [
        {"parity": "2"},
        {"spin_z_x2": "-2"},
        {"isospin_z_x2": "-2"},
    ]


class Hadron4DTestCase(Hadron4DParser, BaseTest, TestCase):
    """Tests creation of the Unsmeared link smear.
    """


from lattedb.wavefunction.models import Hadron


class HadronParser(ObjectParser):

    model = Hadron
    _tree = None
    _parameters = {
        "description": "nucleon positive parity spin up upper spin components",
        "strangeness": "0",
        "irrep": "G1",
        "embedding": "1",
        "parity": "1",
        "spin_x2": "1",
        "spin_z_x2": "1",
        "isospin_x2": "1",
        "isospin_z_x2": "1",
        "momentum": "0",
        "nx": 1,
        "ny": 2,
        "nz": 3,
    }

    _consistency_check_changes = [
        {"parity": "2"},
        {"spin_z_x2": "-2"},
        {"isospin_z_x2": "-2"},
    ]


class HadronTestCase(HadronParser, BaseTest, TestCase):
    """Tests creation of the Unsmeared link smear.
    """


class MesonParser(ObjectParser):

    model = Hadron
    _tree = None
    _parameters = {
        "description": "pion ",
        "strangeness": "0",
        "irrep": "A1",
        "embedding": "1",
        "parity": "-1",
        "spin_x2": "0",
        "spin_z_x2": "0",
        "isospin_x2": "1",
        "isospin_z_x2": "1",
        "momentum": "0",
        "nx": 1,
        "ny": 2,
        "nz": 3,
    }


class MesonTestCase(MesonParser, BaseTest, TestCase):
    """Tests creation of the Unsmeared link smear.
    """
