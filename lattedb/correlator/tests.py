"""Unittests for the correlator module
"""
from django.test import TestCase
from espressodb.base.exceptions import ConsistencyError

from lattedb.utilities.tests import ObjectParser

from lattedb.correlator.models import DWFTuning
from lattedb.propagator.tests import OneToAllTestCaseDWss
from lattedb.propagator.tests import OneToAllTestCaseHisq
from lattedb.wavefunction.tests import MesonTestCase


class DWFTuningTestCase(ObjectParser, TestCase):
    """Tests creation of the Unsmeared link smear.
    """

    model = DWFTuning
    tree = {
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
        "propagator.sinksmear": "GaugeCovariantGaussian",
        "wave": "Hadron",
    }
    parameters = {
        "propagator": OneToAllTestCaseDWss.parameters,
        "wave": MesonTestCase.parameters,
        "sink5": "False",
    }

    consistency_check_changes = []

    def create_default_object(self, ClassObject):
        classobject = ClassObject()
        parameters = classobject.parameters
        tree = classobject.tree
        object, _ = classobject.create_instance(parameters=parameters, tree=tree)
        return object

    def test_propagator_type_consistency(self):
        """Write unittest when another fundamental propagator is defined
        """

    def test_fermionaction_type_consistency(self):
        """Test that fermion action is domain wall type
        """
        propagator = self.create_default_object(OneToAllTestCaseHisq)
        wave = self.create_default_object(MesonTestCase)

        parameters = dict(self.parameters)
        parameters["propagator"] = propagator
        parameters["wave"] = wave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)


from lattedb.correlator.models import Meson2pt
from lattedb.propagator.tests import OneToAllTestCaseDW


class Meson2ptTestCase(ObjectParser, TestCase):
    """
    Test meson two point correlator table.
    The source and sink interpolating operators are not checked to be the same on purpose.
    """

    model = Meson2pt
    tree = {
        "propagator0": "OneToAll",
        "propagator0.gaugeconfig": "Nf211",
        "propagator0.gaugeconfig.gaugeaction": "LuescherWeisz",
        "propagator0.gaugeconfig.light": "Hisq",
        "propagator0.gaugeconfig.strange": "Hisq",
        "propagator0.gaugeconfig.charm": "Hisq",
        "propagator0.gaugeconfig.light.linksmear": "Unsmeared",
        "propagator0.gaugeconfig.strange.linksmear": "Unsmeared",
        "propagator0.gaugeconfig.charm.linksmear": "Unsmeared",
        "propagator0.fermionaction": "MobiusDW",
        "propagator0.fermionaction.linksmear": "WilsonFlow",
        "propagator0.sourcesmear": "GaugeCovariantGaussian",
        "propagator0.sinksmear": "GaugeCovariantGaussian",
        "propagator1": "OneToAll",
        "propagator1.gaugeconfig": "Nf211",
        "propagator1.gaugeconfig.gaugeaction": "LuescherWeisz",
        "propagator1.gaugeconfig.light": "Hisq",
        "propagator1.gaugeconfig.strange": "Hisq",
        "propagator1.gaugeconfig.charm": "Hisq",
        "propagator1.gaugeconfig.light.linksmear": "Unsmeared",
        "propagator1.gaugeconfig.strange.linksmear": "Unsmeared",
        "propagator1.gaugeconfig.charm.linksmear": "Unsmeared",
        "propagator1.fermionaction": "MobiusDW",
        "propagator1.fermionaction.linksmear": "WilsonFlow",
        "propagator1.sourcesmear": "GaugeCovariantGaussian",
        "propagator1.sinksmear": "GaugeCovariantGaussian",
        "sourcewave": "Hadron",
        "sinkwave": "Hadron",
    }
    parameters = {
        "propagator0": OneToAllTestCaseDWss.parameters,
        "propagator1": OneToAllTestCaseDWss.parameters,
        "sourcewave": MesonTestCase.parameters,
        "sinkwave": MesonTestCase.parameters,
    }
    consistency_check_changes = []

    def create_default_object(self, ClassObject):
        classobject = ClassObject()
        parameters = classobject.parameters
        tree = classobject.tree
        object, _ = classobject.create_instance(parameters=parameters, tree=tree)
        return object

    def test_propagator_type_consistency(self):
        """
        Write this when a fundamental propagator type is defined.
        """

    def test_propagator_id_order_consistency(self):
        prop1 = self.create_default_object(OneToAllTestCaseHisq)
        prop0 = self.create_default_object(OneToAllTestCaseDWss)
        sourcewave = self.create_default_object(MesonTestCase)
        sinkwave = self.create_default_object(MesonTestCase)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_gaugeconfig_id_consistency(self):
        prop0 = self.create_default_object(OneToAllTestCaseDW)
        classobject = OneToAllTestCaseDW()
        clsparameters = classobject.parameters
        clstree = classobject.tree
        clsparameters["gaugeconfig"]["config"] = (
            int(clsparameters["gaugeconfig"]["config"]) + 10
        )
        prop1, _ = classobject.create_instance(parameters=clsparameters, tree=clstree)
        sourcewave = self.create_default_object(MesonTestCase)
        sinkwave = self.create_default_object(MesonTestCase)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_sourcesmear_id_consistency(self):
        classobject = OneToAllTestCaseDWss()
        tree = dict(classobject.tree)
        tree["sourcesmear"] = "Point"
        prop0, _ = classobject.create_instance(tree=tree)
        prop1 = self.create_default_object(OneToAllTestCaseDWss)
        sourcewave = self.create_default_object(MesonTestCase)
        sinkwave = self.create_default_object(MesonTestCase)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_sinksmear_id_consistency(self):
        prop0 = self.create_default_object(OneToAllTestCaseDW)
        prop1 = self.create_default_object(OneToAllTestCaseDWss)
        sourcewave = self.create_default_object(MesonTestCase)
        sinkwave = self.create_default_object(MesonTestCase)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)


from lattedb.correlator.models import Baryon2pt
from lattedb.wavefunction.tests import HadronTestCase


class Baryon2ptTestCase(ObjectParser, TestCase):
    model = Baryon2pt
    tree = {
        "propagator0": "OneToAll",
        "propagator0.gaugeconfig": "Nf211",
        "propagator0.gaugeconfig.gaugeaction": "LuescherWeisz",
        "propagator0.gaugeconfig.light": "Hisq",
        "propagator0.gaugeconfig.strange": "Hisq",
        "propagator0.gaugeconfig.charm": "Hisq",
        "propagator0.gaugeconfig.light.linksmear": "Unsmeared",
        "propagator0.gaugeconfig.strange.linksmear": "Unsmeared",
        "propagator0.gaugeconfig.charm.linksmear": "Unsmeared",
        "propagator0.fermionaction": "MobiusDW",
        "propagator0.fermionaction.linksmear": "WilsonFlow",
        "propagator0.sourcesmear": "GaugeCovariantGaussian",
        "propagator0.sinksmear": "GaugeCovariantGaussian",
        "propagator1": "OneToAll",
        "propagator1.gaugeconfig": "Nf211",
        "propagator1.gaugeconfig.gaugeaction": "LuescherWeisz",
        "propagator1.gaugeconfig.light": "Hisq",
        "propagator1.gaugeconfig.strange": "Hisq",
        "propagator1.gaugeconfig.charm": "Hisq",
        "propagator1.gaugeconfig.light.linksmear": "Unsmeared",
        "propagator1.gaugeconfig.strange.linksmear": "Unsmeared",
        "propagator1.gaugeconfig.charm.linksmear": "Unsmeared",
        "propagator1.fermionaction": "MobiusDW",
        "propagator1.fermionaction.linksmear": "WilsonFlow",
        "propagator1.sourcesmear": "GaugeCovariantGaussian",
        "propagator1.sinksmear": "GaugeCovariantGaussian",
        "propagator2": "OneToAll",
        "propagator2.gaugeconfig": "Nf211",
        "propagator2.gaugeconfig.gaugeaction": "LuescherWeisz",
        "propagator2.gaugeconfig.light": "Hisq",
        "propagator2.gaugeconfig.strange": "Hisq",
        "propagator2.gaugeconfig.charm": "Hisq",
        "propagator2.gaugeconfig.light.linksmear": "Unsmeared",
        "propagator2.gaugeconfig.strange.linksmear": "Unsmeared",
        "propagator2.gaugeconfig.charm.linksmear": "Unsmeared",
        "propagator2.fermionaction": "MobiusDW",
        "propagator2.fermionaction.linksmear": "WilsonFlow",
        "propagator2.sourcesmear": "GaugeCovariantGaussian",
        "propagator2.sinksmear": "GaugeCovariantGaussian",
        "sourcewave": "Hadron",
        "sinkwave": "Hadron",
    }
    parameters = {
        "propagator0": OneToAllTestCaseDWss.parameters,
        "propagator1": OneToAllTestCaseDWss.parameters,
        "propagator2": OneToAllTestCaseDWss.parameters,
        "sourcewave": HadronTestCase.parameters,
        "sinkwave": HadronTestCase.parameters,
    }
    consistency_check_changes = []

    def create_default_object(self, ClassObject):
        classobject = ClassObject()
        parameters = classobject.parameters
        tree = classobject.tree
        object, _ = classobject.create_instance(parameters=parameters, tree=tree)
        return object

    def test_propagator_type_consistency(self):
        """
        Write this when a fundamental propagator type is defined.
        """

    def test_propagator_id_order_consistency(self):
        prop1 = self.create_default_object(OneToAllTestCaseHisq)
        prop0 = self.create_default_object(OneToAllTestCaseDWss)
        prop2 = self.create_default_object(OneToAllTestCaseDWss)
        sourcewave = self.create_default_object(HadronTestCase)
        sinkwave = self.create_default_object(HadronTestCase)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["propagator2"] = prop2
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_gaugeconfig_id_consistency(self):
        prop0 = self.create_default_object(OneToAllTestCaseDW)
        classobject = OneToAllTestCaseDW()
        clsparameters = classobject.parameters
        clstree = classobject.tree
        clsparameters["gaugeconfig"]["config"] = (
            int(clsparameters["gaugeconfig"]["config"]) + 10
        )
        prop1, _ = classobject.create_instance(parameters=clsparameters, tree=clstree)
        prop2 = self.create_default_object(OneToAllTestCaseDW)
        sourcewave = self.create_default_object(MesonTestCase)
        sinkwave = self.create_default_object(MesonTestCase)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["propagator2"] = prop2
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_sourcesmear_id_consistency(self):
        classobject = OneToAllTestCaseDWss()
        tree = dict(classobject.tree)
        tree["sourcesmear"] = "Point"
        prop0, _ = classobject.create_instance(tree=tree)
        prop1 = self.create_default_object(OneToAllTestCaseDWss)
        prop2 = self.create_default_object(OneToAllTestCaseDWss)
        sourcewave = self.create_default_object(MesonTestCase)
        sinkwave = self.create_default_object(MesonTestCase)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["propagator2"] = prop2
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_sinksmear_id_consistency(self):
        prop0 = self.create_default_object(OneToAllTestCaseDW)
        prop1 = self.create_default_object(OneToAllTestCaseDWss)
        prop2 = self.create_default_object(OneToAllTestCaseDWss)
        sourcewave = self.create_default_object(MesonTestCase)
        sinkwave = self.create_default_object(MesonTestCase)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["propagator2"] = prop2
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)


from lattedb.correlator.models import BaryonFH3pt

# class BaryonFH3ptTestCase(ObjectParser, TestCase):
#    model = BaryonFH3pt
#    tree = {
#        "sourcewave": "Hadron",
#        "sinkwave": "Hadron",
#        "fhpropagator": "FeynmanHellmann",
#        "propagator0": "OneToAll",
#        "propagator1": "OneToAll",
#    }
#    parameters = {
#
#    }
