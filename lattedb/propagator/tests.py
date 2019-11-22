"""
Unittests for the propagator module
"""

from django.test import TestCase
from espressodb.base.models import ConsistencyError

from lattedb.utilities.tests import ObjectParser

from lattedb.propagator.models import OneToAll
from lattedb.gaugeconfig.tests import Nf211TestCaseHisq
from lattedb.gaugeconfig.tests import Nf211TestCaseHisqAlt
from lattedb.fermionaction.tests import MobiusDWTestCaseLightWF
from lattedb.fermionaction.tests import HisqTestCaseLightWF
from lattedb.quarksmear.tests import PointTestCase
from lattedb.quarksmear.tests import GaugeCovariantGaussianTestCase


class OneToAllTestCaseDW(ObjectParser, TestCase):
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
        "gaugeconfig": Nf211TestCaseHisq.parameters,
        "fermionaction": MobiusDWTestCaseLightWF.parameters,
        "origin_x": "2",
        "origin_y": "10",
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

class OneToAllTestCaseDWAlt(ObjectParser, TestCase):
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
        "gaugeconfig": Nf211TestCaseHisqAlt.parameters,
        "fermionaction": MobiusDWTestCaseLightWF.parameters,
        "origin_x": "2",
        "origin_y": "10",
        "origin_z": "8",
        "origin_t": "6",
        "sourcesmear": GaugeCovariantGaussianTestCase.parameters,
        "sinksmear": PointTestCase.parameters,
    }

class OneToAllTestCaseHisq(ObjectParser, TestCase):
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
        "fermionaction": "Hisq",
        "fermionaction.linksmear": "Unsmeared",
        "sourcesmear": "GaugeCovariantGaussian",
        "sinksmear": "Point",
    }
    parameters = {
        "gaugeconfig": Nf211TestCaseHisq.parameters,
        "fermionaction": HisqTestCaseLightWF.parameters,
        "origin_x": "2",
        "origin_y": "10",
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
        "gaugeconfig": Nf211TestCaseHisq.parameters,
        "fermionaction": MobiusDWTestCaseLightWF.parameters,
        "sinkwave": HadronTestCase.parameters,
        "sinksmear": PointTestCase.parameters,
        "sinksep": "10",
    }
    consistency_check_changes = []

    def test_default_creation(self, parameters=None, tree=None):
        pass

    def test_inconsistent_creation(self):
        pass

    def first_pair(self):
        baryoncoherentseq, _ = self.create_instance()

        onetoalltestcase = OneToAllTestCaseDW()
        prop, _ = onetoalltestcase.create_instance()
        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)
        baryoncoherentseq.save()

        # prep next prop
        return baryoncoherentseq

    def test_many_to_many(self):
        """Tests creation of many to many field which should not fail
        """
        baryoncoherentseq = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        onetoallparameters = dict(onetoalltestcase.parameters)
        onetoallparameters["origin_x"] = int(onetoallparameters["origin_x"]) + 5
        onetoallparameters["origin_y"] = int(onetoallparameters["origin_y"]) + 3
        onetoallparameters["origin_z"] = int(onetoallparameters["origin_z"]) + 1
        onetoallparameters["origin_t"] = int(onetoallparameters["origin_x"]) + 8
        prop, _ = onetoalltestcase.create_instance(parameters=onetoallparameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)
        baryoncoherentseq.save()

    def test_prop_length_consistency(self):
        """Tests creation of many to many field which should fail
        """
        baryoncoherentseq, prop = self.first_pair()

        prop.save()

        baryoncoherentseq.propagator0.add(prop)
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()

    def test_prop_type_consistency(self):
        """
        Need to write test if another fundamental prop type is defined.
        This unittest checks if the spectators are all OneToAll.
        """

    def test_prop_fermionaction_type_consistency(self):
        baryoncoherentseq, prop = self.first_pair()

        onetoalltestcasehisq = OneToAllTestCaseHisq()
        prop , _= onetoalltestcasehisq.create_instance()

        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()

    def test_prop_config_id_consistency(self):
        baryoncoherentseq, prop = self.first_pair()

        prop.save()
        baryoncoherentseq.propagator0.add(prop)

        onetoalltestcasedwalt = OneToAllTestCaseDWAlt()
        prop, _ = onetoalltestcasedwalt.create_instance()
        prop.origin_x += 5
        prop.origin_y += 3
        prop.origin_z += 1
        prop.origin_t += 8
        prop.id += 1
        prop.save()

        baryoncoherentseq.propagator1.add(prop)

        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()
