"""Unittests for the quarksmear module
"""
from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.wavefunction.models import Hadron4D


class Hadron4DTestCase(ObjectParser, TestCase):
    """Tests creation of the Unsmeared link smear.
    """

    model = Hadron4D
    tree = None
    parameters = {
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

    consistency_check_changes = [
        {"parity": "2"},
        {"spin_z_x2": "-2"},
        {"isospin_z_x2": "-2"},
    ]


from lattedb.wavefunction.models import Hadron


class HadronTestCase(ObjectParser, TestCase):
    """Tests creation of the Unsmeared link smear.
    """

    model = Hadron
    tree = None
    parameters = {
        "description": "iddqd",
        "strangeness": "0",
        "irrep": "G1",
        "embedding": "1",
        "parity": "1",
        "spin_x2": "1",
        "spin_z_x2": "1",
        "isospin_x2": "1",
        "isospin_z_x2": "1",
        "momentum": "0",
    }

    consistency_check_changes = [
        {"parity": "2"},
        {"spin_z_x2": "-2"},
        {"isospin_z_x2": "-2"},
    ]
