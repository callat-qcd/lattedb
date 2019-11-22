"""
Unittests for the propagator module
"""

from django.test import TestCase

from lattedb.utilities.tests import ObjectParser

from lattedb.propagator.models import OneToAll
from lattedb.gaugeconfig.tests import Nf211TestCase
from lattedb.fermionaction.tests import MobiusDWTestCaseLightWF
from lattedb.quarksmear.tests import PointTestCase
from lattedb.quarksmear.tests import GaugeCovariantGaussianTestCase


class OneToAllTestCase(ObjectParser, TestCase):
    model = OneToAll
    tree = {
        "gaugeconfig": "Nf211",
        "gaugeconfig.gaugeaction": "LuescherWeisz",
        "gaugeconfig.light": "Hisq",
        "gaugeconfig.strange": "Hisq",
        "gaugeconfig.charm": "Hisq",
        "gaugeconfig.light.linksmear": "Unsmeared",
        "gaugeconfig.strange.linksmear": "Unsmeared",
        "gaugeconfig.charm.linksmear": "Unsmeared",
        "fermionaction": "MobiusDW",
        "fermionaction.linksmear": "WilsonFlow",
        "sourcesmear": "GaugeCovariantGaussian",
        "sinksmear": "Point",
    }
    parameters = {
        "gaugeconfig": Nf211TestCase.parameters,
        "fermionaction": MobiusDWTestCaseLightWF.parameters,
        "origin_x": "2",
        "origin_y": "20",
        "origin_z": "8",
        "origin_t": "6",
        "sourcesmear": GaugeCovariantGaussianTestCase.parameters,
        "sinksmear": PointTestCase.parameters,
    }
    consistency_check_changes = [
        {"origin_x": "10000"},
        {"origin_y": "10000"},
        {"origin_z": "10000"},
        {"origin_t": "10000"},
    ]


from lattedb.propagator.models import BaryonCoherentSeq
from lattedb.wavefunction.tests import HadronTestCase

class BaryonCoherentSeqTestCase(ObjectParser, TestCase):
    model = BaryonCoherentSeq
    tree = {
        "gaugeconfig": "Nf211",
        "gaugeconfig.gaugeaction": "LuescherWeisz",
        "gaugeconfig.light": "Hisq",
        "gaugeconfig.strange": "Hisq",
        "gaugeconfig.charm": "Hisq",
        "gaugeconfig.light.linksmear": "Unsmeared",
        "gaugeconfig.strange.linksmear": "Unsmeared",
        "gaugeconfig.charm.linksmear": "Unsmeared",
        "fermionaction": "MobiusDW",
        "fermionaction.linksmear": "WilsonFlow",
        "sinkwave": "Hadron",
        "sinksmear": "Point",
    }
    parameters = {
        "gaugeconfig": Nf211TestCase.parameters,
        "fermionaction": MobiusDWTestCaseLightWF.parameters,
        "sinkwave": HadronTestCase.parameters,
        "sinksmear": PointTestCase.parameters,
        "sinksep": "10",
    }
    consistency_check_changes = []

    def test_default_creation(self, parameters, tree):
        pass

    def test_inconsistent_creation(self):
        pass

    def test_many_to_many(self):
        """Tests creation of many to many field which should not fail
        """
        baryoncoherentseq, _ = self.create_instance()

        onetoalltestcase = OneToAllTestCase()
        prop = onetoalltestcase.test_default_creation()
        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)
        baryoncoherentseq.save()

        prop.id += 1
        prop.origin_x += 5
        prop.origin_y += 3
        prop.origin_z += 1
        prop.origin_t += 8
        prop.save()
        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)
        baryoncoherentseq.save()
