"""
Unittests for the propagator module
"""

from django.test import TestCase
from espressodb.base.models import ConsistencyError

from lattedb.utilities.tests import ObjectParser

from lattedb.propagator.models import OneToAll
from lattedb.gaugeconfig.tests import Nf211TestCaseHisq
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
        onetoallparameters["origin_t"] = int(onetoallparameters["origin_t"]) + 8
        prop, _ = onetoalltestcase.create_instance(parameters=onetoallparameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)
        baryoncoherentseq.save()

    def test_prop_length_consistency(self):
        """Tests creation of many to many field which should fail
        """
        baryoncoherentseq = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        onetoallparameters = dict(onetoalltestcase.parameters)
        onetoallparameters["origin_t"] = int(onetoallparameters["origin_t"]) + 8
        prop, _ = onetoalltestcase.create_instance(parameters=onetoallparameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator0.add(prop)
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()
        print(context.exception.error)

    def test_prop_type_consistency(self):
        """
        Need to write test if another fundamental prop type is defined.
        This unittest checks if the spectators are all OneToAll.
        """

    def test_prop_fermionaction_type_consistency(self):
        baryoncoherentseq = self.first_pair()

        onetoalltestcasehisq = OneToAllTestCaseHisq()
        prop , _= onetoalltestcasehisq.create_instance()

        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()
        print(context.exception.error)

    def test_prop_config_id_consistency(self):
        baryoncoherentseq = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["gaugeconfig"]["config"] = int(parameters["gaugeconfig"]["config"]) + 5
        prop, _ = onetoalltestcase.create_instance(parameters=parameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)

        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()
        print(context.exception.error)

    def test_prop_sourcesmear_consistency(self):
        baryoncoherentseq = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["sourcesmear"]["step"] = 1000
        prop, _ = onetoalltestcase.create_instance(parameters=parameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)

        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()
        print(context.exception.error)

    def test_prop_sinksmear_consistency(self):
        baryoncoherentseq = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["sinksmear"]["radius"] = "3.0"
        parameters["sinksmear"]["step"] = "30"
        tree = dict(onetoalltestcase.tree)
        tree["sinksmear"] = "GaugeCovariantGaussian"
        prop, _ = onetoalltestcase.create_instance(parameters=parameters, tree=tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator0.add(prop)
        baryoncoherentseq.propagator1.add(prop)

        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()
        print(context.exception.error)

    def test_prop_id_sequence_consistency(self):
        baryoncoherentseq = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8

        prop, _ = onetoalltestcase.create_instance(parameters=parameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator1.add(prop)

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["fermionaction"]["quark_mass"] = "0.5"
        parameters["fermionaction"]["quark_tag"] = "strange"

        prop, _ = onetoalltestcase.create_instance(parameters=parameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 3)

        baryoncoherentseq.propagator0.add(prop)

        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()
        print(context.exception.error)

    def test_prop_origin_consistency(self):
        baryoncoherentseq = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8

        prop, _ = onetoalltestcase.create_instance(parameters=parameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        baryoncoherentseq.propagator0.add(prop)

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 9

        prop, _ = onetoalltestcase.create_instance(parameters=parameters, tree=onetoalltestcase.tree)

        self.assertEqual(OneToAll.objects.all().count(), 3)

        baryoncoherentseq.propagator1.add(prop)

        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.save()
        print(context.exception.error)

from lattedb.propagator.models import FeynmanHellmann
from lattedb.current.tests import LocalTestCase

class FeynmanHellmannTestCase(ObjectParser, TestCase):
    model = FeynmanHellmann
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
        "propagator": "OneToAll",
        "propagator.gaugeconfig": "Nf211",
        "propagator.gaugeconfig.gaugeaction": "LuescherWeisz",
        "propagator.gaugeconfig.light": "Hisq",
        "propagator.gaugeconfig.strange": "Hisq",
        "propagator.gaugeconfig.charm": "Hisq",
        "propagator.gaugeconfig.light.linksmear": "Unsmeared",
        "propagator.gaugeconfig.strange.linksmear": "Unsmeared",
        "propagator.gaugeconfig.charm.linksmear": "Unsmeared",
        "propagator.fermionaction": "MobiusDW",
        "propagator.fermionaction.linksmear": "WilsonFlow",
        "propagator.sourcesmear": "GaugeCovariantGaussian",
        "propagator.sinksmear": "Point",
        "current": "Local",
        "sinksmear": "GaugeCovariantGaussian",
    }
    parameters = {
        "gaugeconfig": Nf211TestCaseHisq.parameters,
        "fermionaction": MobiusDWTestCaseLightWF.parameters,
        "propagator": OneToAllTestCaseDW.parameters,
        "current": LocalTestCase.parameters,
        "sinksmear": GaugeCovariantGaussianTestCase.parameters,
    }
    consistency_check_changes = [
    ]