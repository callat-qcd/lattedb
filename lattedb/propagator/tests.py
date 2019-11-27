"""
Unittests for the propagator module
"""

from django.test import TestCase
from django.db.models import Q
from espressodb.base.exceptions import ConsistencyError

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


class OneToAllTestCaseDWss(ObjectParser, TestCase):
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
        "sinksmear": "GaugeCovariantGaussian",
    }
    parameters = {
        "gaugeconfig": Nf211TestCaseHisq.parameters,
        "fermionaction": MobiusDWTestCaseLightWF.parameters,
        "origin_x": "2",
        "origin_y": "10",
        "origin_z": "8",
        "origin_t": "6",
        "sourcesmear": GaugeCovariantGaussianTestCase.parameters,
        "sinksmear": GaugeCovariantGaussianTestCase.parameters,
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
        "sinksmear": "GaugeCovariantGaussian",
    }
    parameters = {
        "gaugeconfig": Nf211TestCaseHisq.parameters,
        "fermionaction": HisqTestCaseLightWF.parameters,
        "origin_x": "2",
        "origin_y": "10",
        "origin_z": "8",
        "origin_t": "6",
        "sourcesmear": GaugeCovariantGaussianTestCase.parameters,
        "sinksmear": GaugeCovariantGaussianTestCase.parameters,
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
        **{f"gaugeconfig.{key}": val for key, val in Nf211TestCaseHisq.tree.items()},
        "fermionaction": "MobiusDW",
        "fermionaction.linksmear": "WilsonFlow",
        "sinkwave": "Hadron",
        "sinksmear": "Point",
        "propagator0": "OneToAll",
        "propagator0.gaugeconfig": "Hisq",
    }
    # m2m_tree = {
    # "propagator0": [{"OneToAll":
    # {"gaugeconfig": "Hisq", "fermionaction":"Domainwall", "ÖneToAll"}}]    }
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

    @classmethod
    def first_pair(cls):
        onetoalltestcase = OneToAllTestCaseDW()
        prop, _ = onetoalltestcase.create_instance()
        return prop
    @classmethod
    def create_populated_instance(cls):
        """
        """
        baryoncoherentseq, _ = cls.create_instance()
        prop0 = cls.first_pair()
        onetoalltestcase = OneToAllTestCaseDW()
        onetoallparameters = dict(onetoalltestcase.parameters)
        onetoallparameters["origin_t"] = int(onetoallparameters["origin_t"]) + 8
        prop1, _ = onetoalltestcase.create_instance(
            parameters=onetoallparameters, tree=onetoalltestcase.tree
        )
        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        baryoncoherentseq.check_all_consistencies(props0, props1)
        baryoncoherentseq.propagator0.add(*props0)
        baryoncoherentseq.propagator1.add(*props1)
        return baryoncoherentseq

    def test_many_to_many(self):
        """Tests creation of many to many field and unique constraint
        """
        baryoncoherentseq = self.create_populated_instance()
        props0 = baryoncoherentseq.propagator0.all()
        props1 = baryoncoherentseq.propagator1.all()

        # check unique constraint
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_length_consistency(self):
        """Tests creation of many to many field which should fail
        """
        baryoncoherentseq, _ = self.create_instance()

        prop0 = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        onetoallparameters = dict(onetoalltestcase.parameters)
        onetoallparameters["origin_t"] = int(onetoallparameters["origin_t"]) + 8
        prop1, _ = onetoalltestcase.create_instance(
            parameters=onetoallparameters, tree=onetoalltestcase.tree
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = OneToAll.objects.filter(Q(pk=prop0.pk))
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_type_consistency(self):
        """
        Need to write test if another fundamental prop type is defined.
        This unittest checks if the spectators are all OneToAll.
        """

    def test_prop_fermionaction_type_consistency(self):
        baryoncoherentseq, _ = self.create_instance()

        prop0 = self.first_pair()

        onetoalltestcasehisq = OneToAllTestCaseHisq()
        prop1, _ = onetoalltestcasehisq.create_instance()

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_config_id_consistency(self):
        baryoncoherentseq, _ = self.create_instance()

        prop0 = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["gaugeconfig"]["config"] = (
            int(parameters["gaugeconfig"]["config"]) + 5
        )
        prop1, _ = onetoalltestcase.create_instance(
            parameters=parameters, tree=onetoalltestcase.tree
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_sourcesmear_consistency(self):
        baryoncoherentseq, _ = self.create_instance()

        prop0 = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["sourcesmear"]["step"] = 1000
        prop1, _ = onetoalltestcase.create_instance(
            parameters=parameters, tree=onetoalltestcase.tree
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_sinksmear_consistency(self):
        baryoncoherentseq, _ = self.create_instance()

        prop0 = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["sinksmear"]["radius"] = "3.0"
        parameters["sinksmear"]["step"] = "30"
        tree = dict(onetoalltestcase.tree)
        tree["sinksmear"] = "GaugeCovariantGaussian"
        prop1, _ = onetoalltestcase.create_instance(parameters=parameters, tree=tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_id_sequence_consistency(self):
        baryoncoherentseq, _ = self.create_instance()

        prop0 = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8

        prop1, _ = onetoalltestcase.create_instance(
            parameters=parameters, tree=onetoalltestcase.tree
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["fermionaction"]["quark_mass"] = "0.5"
        parameters["fermionaction"]["quark_tag"] = "strange"

        prop2, _ = onetoalltestcase.create_instance(
            parameters=parameters, tree=onetoalltestcase.tree
        )

        self.assertEqual(OneToAll.objects.all().count(), 3)

        props0 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop2.pk))
        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_origin_consistency(self):
        baryoncoherentseq, _ = self.create_instance()

        prop0 = self.first_pair()

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 8

        prop1, _ = onetoalltestcase.create_instance(
            parameters=parameters, tree=onetoalltestcase.tree
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        onetoalltestcase = OneToAllTestCaseDW()
        parameters = dict(onetoalltestcase.parameters)
        parameters["origin_t"] = int(parameters["origin_t"]) + 9

        prop2, _ = onetoalltestcase.create_instance(
            parameters=parameters, tree=onetoalltestcase.tree
        )

        self.assertEqual(OneToAll.objects.all().count(), 3)

        props0 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop2.pk))
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
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
    consistency_check_changes = []

    def create_default_object(self, ClassObject):
        classobject = ClassObject()
        parameters = classobject.parameters
        tree = classobject.tree
        object, _ = classobject.create_instance(parameters=parameters, tree=tree)
        return object

    def test_prop_type_consistency(self):
        """
        Make unit test when another fundamental prop type exists.
        """

    def test_gaugeconfig_id_consistency(self):
        nf211testcasehisq = Nf211TestCaseHisq()
        gaugeconfigparameters = dict(nf211testcasehisq.parameters)
        gaugeconfigparameters["config"] = int(gaugeconfigparameters["config"]) + 5
        gaugeconfig, _ = nf211testcasehisq.create_instance(
            parameters=gaugeconfigparameters, tree=nf211testcasehisq.tree
        )
        fermionaction = self.create_default_object(MobiusDWTestCaseLightWF)
        propagator = self.create_default_object(OneToAllTestCaseDW)
        current = self.create_default_object(LocalTestCase)
        sinksmear = self.create_default_object(GaugeCovariantGaussianTestCase)

        parameters = dict(self.parameters)
        parameters["gaugeconfig"] = gaugeconfig
        parameters["fermionaction"] = fermionaction
        parameters["propagator"] = propagator
        parameters["current"] = current
        parameters["sinksmear"] = sinksmear

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_fermionaction_type_consistency(self):
        gaugeconfig = self.create_default_object(Nf211TestCaseHisq)
        fermiontc = HisqTestCaseLightWF
        fermionparameters = dict(fermiontc.parameters)
        fermiontree = fermiontc.tree
        fermionaction, _ = fermiontc.create_instance(
            parameters=fermionparameters, tree=fermiontree
        )
        propagator = self.create_default_object(OneToAllTestCaseDW)
        current = self.create_default_object(LocalTestCase)
        sinksmear = self.create_default_object(GaugeCovariantGaussianTestCase)

        parameters = dict(self.parameters)
        parameters["gaugeconfig"] = gaugeconfig
        parameters["fermionaction"] = fermionaction
        parameters["propagator"] = propagator
        parameters["current"] = current
        parameters["sinksmear"] = sinksmear

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_prop_sinksmear_consistency(self):
        gaugeconfig = self.create_default_object(Nf211TestCaseHisq)
        fermionaction = self.create_default_object(MobiusDWTestCaseLightWF)
        propagator = self.create_default_object(OneToAllTestCaseDWss)
        current = self.create_default_object(LocalTestCase)
        sinksmear = self.create_default_object(GaugeCovariantGaussianTestCase)

        parameters = dict(self.parameters)
        parameters["gaugeconfig"] = gaugeconfig
        parameters["fermionaction"] = fermionaction
        parameters["propagator"] = propagator
        parameters["current"] = current
        parameters["sinksmear"] = sinksmear

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)
