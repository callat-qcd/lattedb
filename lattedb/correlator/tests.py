"""Unittests for the correlator module
"""
from django.test import TestCase
from espressodb.base.models import ConsistencyError

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
        "sink5": "False"
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