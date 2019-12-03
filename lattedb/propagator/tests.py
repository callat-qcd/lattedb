"""
Unittests for the propagator module
"""

from django.test import TestCase
from django.db.models import Q
from espressodb.base.exceptions import ConsistencyError

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.propagator.models import OneToAll

from lattedb.gaugeconfig.tests import Nf211HisqParser
from lattedb.fermionaction.tests import MobiusDWLightWFParser
from lattedb.fermionaction.tests import HisqLightWFParser
from lattedb.quarksmear.tests import PointParser
from lattedb.quarksmear.tests import GaugeCovariantGaussianParser


class OneToAllDWParser(ObjectParser):
    model = OneToAll
    _tree = {
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
    _parameters = {
        "gaugeconfig": Nf211HisqParser.get_parameters(),
        "fermionaction": MobiusDWLightWFParser.get_parameters(),
        "origin_x": "2",
        "origin_y": "10",
        "origin_z": "8",
        "origin_t": "6",
        "sourcesmear": GaugeCovariantGaussianParser.get_parameters(),
        "sinksmear": PointParser.get_parameters(),
    }
    _consistency_check_changes = [
        {"origin_x": "10000"},
        {"origin_y": "10000"},
        {"origin_z": "10000"},
        {"origin_t": "10000"},
    ]


class OneToAllDWTestCase(OneToAllDWParser, BaseTest, TestCase):
    ""


class OneToAllDWssParser(ObjectParser, BaseTest, TestCase):
    model = OneToAll
    _tree = {
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
    _parameters = {
        "gaugeconfig": Nf211HisqParser.get_parameters(),
        "fermionaction": MobiusDWLightWFParser.get_parameters(),
        "origin_x": "2",
        "origin_y": "10",
        "origin_z": "8",
        "origin_t": "6",
        "sourcesmear": GaugeCovariantGaussianParser.get_parameters(),
        "sinksmear": GaugeCovariantGaussianParser.get_parameters(),
    }


class OneToAllDWssTestCase(OneToAllDWssParser, BaseTest, TestCase):
    ""


class OneToAllHisqParser(ObjectParser):
    model = OneToAll
    _tree = {
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
    _parameters = {
        "gaugeconfig": Nf211HisqParser.get_parameters(),
        "fermionaction": HisqLightWFParser.get_parameters(),
        "origin_x": "2",
        "origin_y": "10",
        "origin_z": "8",
        "origin_t": "6",
        "sourcesmear": GaugeCovariantGaussianParser.get_parameters(),
        "sinksmear": GaugeCovariantGaussianParser.get_parameters(),
    }
    _consistency_check_changes = [
        {"origin_x": "10000"},
        {"origin_y": "10000"},
        {"origin_z": "10000"},
        {"origin_t": "10000"},
    ]


class OneToAllHisqTestCase(OneToAllHisqParser, BaseTest, TestCase):
    ""


from lattedb.propagator.models import BaryonCoherentSeq
from lattedb.wavefunction.tests import HadronTestCase


class BaryonCoherentSeqParser(ObjectParser):
    model = BaryonCoherentSeq
    _tree = {
        "gaugeconfig": "Nf211",
        **{
            f"gaugeconfig.{key}": val for key, val in Nf211HisqParser.get_tree().items()
        },
        "fermionaction": "MobiusDW",
        "fermionaction.linksmear": "WilsonFlow",
        "sinkwave": "Hadron",
        "sinksmear": "Point",
        "propagator0": "OneToAll",
        "propagator0.gaugeconfig": "Hisq",
    }
    _parameters = {
        "gaugeconfig": Nf211HisqParser.get_parameters(),
        "fermionaction": MobiusDWLightWFParser.get_parameters(),
        "sinkwave": HadronTestCase.get_parameters(),
        "sinksmear": PointParser.get_parameters(),
        "sinksep": "10",
    }

    @classmethod
    def first_pair(cls):
        return OneToAllDWParser.create_instance()

    @classmethod
    def create_populated_instance(cls):
        """
        """
        baryoncoherentseq = cls.create_instance()
        prop0 = cls.first_pair()
        onetoall_parameters = OneToAllDWParser.get_parameters()
        onetoall_parameters["origin_t"] = int(onetoall_parameters["origin_t"]) + 8
        prop1 = OneToAllDWParser.create_instance(
            parameters=onetoall_parameters, tree=OneToAllDWParser.get_tree()
        )
        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        baryoncoherentseq.check_all_consistencies(props0, props1)
        baryoncoherentseq.propagator0.add(*props0)
        baryoncoherentseq.propagator1.add(*props1)
        return baryoncoherentseq

class BaryonCoherentSeqTestCase(BaryonCoherentSeqParser, TestCase):
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
        baryoncoherentseq = self.create_instance()

        prop0 = self.first_pair()

        onetoall_parameters = OneToAllDWParser.get_parameters()
        onetoall_parameters["origin_t"] = int(onetoall_parameters["origin_t"]) + 8
        prop1 = OneToAllDWParser.create_instance(
            parameters=onetoall_parameters, tree=OneToAllDWParser.get_tree()
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
        baryoncoherentseq = self.create_instance()

        prop0 = self.first_pair()

        prop1 = OneToAllHisqParser.create_instance()

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_config_id_consistency(self):
        baryoncoherentseq = self.create_instance()

        prop0 = self.first_pair()

        parameters = OneToAllHisqParser.get_parameters()
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["gaugeconfig"]["config"] = (
            int(parameters["gaugeconfig"]["config"]) + 5
        )
        prop1 = OneToAllHisqParser.create_instance(
            parameters=parameters, tree=OneToAllHisqParser.get_tree()
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_sourcesmear_consistency(self):
        baryoncoherentseq = self.create_instance()

        prop0 = self.first_pair()

        parameters = OneToAllDWParser.get_parameters()
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["sourcesmear"]["step"] = 1000
        prop1 = OneToAllDWParser.create_instance(
            parameters=parameters, tree=OneToAllDWParser.get_tree()
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_sinksmear_consistency(self):
        baryoncoherentseq = self.create_instance()

        prop0 = self.first_pair()

        parameters = OneToAllDWParser.get_parameters()
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["sinksmear"]["radius"] = "3.0"
        parameters["sinksmear"]["step"] = "30"
        tree = OneToAllDWParser.get_tree()
        tree["sinksmear"] = "GaugeCovariantGaussian"
        prop1 = OneToAllDWParser.create_instance(parameters=parameters, tree=tree)

        self.assertEqual(OneToAll.objects.all().count(), 2)

        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props0 = props1.all()
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_id_sequence_consistency(self):
        baryoncoherentseq = self.create_instance()

        prop0 = self.first_pair()

        parameters = OneToAllDWParser.get_parameters()
        parameters["origin_t"] = int(parameters["origin_t"]) + 8

        prop1 = OneToAllDWParser.create_instance(
            parameters=parameters, tree=OneToAllDWParser.get_tree()
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        parameters = OneToAllDWParser.get_parameters()
        parameters["origin_t"] = int(parameters["origin_t"]) + 8
        parameters["fermionaction"]["quark_mass"] = "0.5"
        parameters["fermionaction"]["quark_tag"] = "strange"

        prop2 = OneToAllDWParser.create_instance(
            parameters=parameters, tree=OneToAllDWParser.get_tree()
        )

        self.assertEqual(OneToAll.objects.all().count(), 3)

        props0 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop2.pk))
        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)

    def test_prop_origin_consistency(self):
        baryoncoherentseq = self.create_instance()

        prop0 = self.first_pair()

        parameters = OneToAllDWParser.get_parameters()
        parameters["origin_t"] = int(parameters["origin_t"]) + 8

        prop1 = OneToAllDWParser.create_instance(
            parameters=parameters, tree=OneToAllDWParser.get_tree()
        )

        self.assertEqual(OneToAll.objects.all().count(), 2)

        parameters = OneToAllDWParser.get_parameters()
        parameters["origin_t"] = int(parameters["origin_t"]) + 9

        prop2 = OneToAllDWParser.create_instance(
            parameters=parameters, tree=OneToAllDWParser.get_tree()
        )

        self.assertEqual(OneToAll.objects.all().count(), 3)

        props0 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop1.pk))
        props1 = OneToAll.objects.filter(Q(pk=prop0.pk) | Q(pk=prop2.pk))
        with self.assertRaises(ConsistencyError) as context:
            baryoncoherentseq.check_all_consistencies(props0, props1)
        print(context.exception.error)


from lattedb.propagator.models import FeynmanHellmann
from lattedb.current.tests import LocalParser


class FeynmanHellmannParser(ObjectParser):
    model = FeynmanHellmann
    _tree = {
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
    _parameters = {
        "gaugeconfig": Nf211HisqParser.get_parameters(),
        "fermionaction": MobiusDWLightWFParser.get_parameters(),
        "propagator": OneToAllDWParser.get_parameters(),
        "current": LocalParser.get_parameters(),
        "sinksmear": GaugeCovariantGaussianParser.get_parameters(),
    }
    _consistency_check_changes = []


class FeynmanHellmannTestCase(FeynmanHellmannParser, BaseTest, TestCase):
    def test_prop_type_consistency(self):
        """
        Make unit test when another fundamental prop type exists.
        """

    def test_gaugeconfig_id_consistency(self):
        gaugeconfig_parameters = Nf211HisqParser.get_parameters()
        gaugeconfig_parameters["config"] = int(gaugeconfig_parameters["config"]) + 5
        gaugeconfig = Nf211HisqParser.create_instance(
            parameters=gaugeconfig_parameters, tree=Nf211HisqParser.get_tree()
        )
        fermionaction = MobiusDWLightWFParser.create_instance()
        propagator = OneToAllDWParser.create_instance()
        current = LocalParser.create_instance()
        sinksmear = GaugeCovariantGaussianParser.create_instance(fail_if_exists=False)

        parameters = self.get_parameters()
        parameters["gaugeconfig"] = gaugeconfig
        parameters["fermionaction"] = fermionaction
        parameters["propagator"] = propagator
        parameters["current"] = current
        parameters["sinksmear"] = sinksmear

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_fermionaction_type_consistency(self):
        gaugeconfig = Nf211HisqParser.create_instance()
        fermionaction = HisqLightWFParser.create_instance()
        propagator = OneToAllDWParser.create_instance()
        current = LocalParser.create_instance()
        sinksmear = GaugeCovariantGaussianParser.create_instance(fail_if_exists=False)

        parameters = self.get_parameters()
        parameters["gaugeconfig"] = gaugeconfig
        parameters["fermionaction"] = fermionaction
        parameters["propagator"] = propagator
        parameters["current"] = current
        parameters["sinksmear"] = sinksmear

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_prop_sinksmear_consistency(self):
        gaugeconfig = Nf211HisqParser.create_instance()
        fermionaction = MobiusDWLightWFParser.create_instance()
        propagator = OneToAllDWssParser.create_instance()
        current = LocalParser.create_instance()
        sinksmear = GaugeCovariantGaussianParser.create_instance(fail_if_exists=False)

        parameters = self.get_parameters()
        parameters["gaugeconfig"] = gaugeconfig
        parameters["fermionaction"] = fermionaction
        parameters["propagator"] = propagator
        parameters["current"] = current
        parameters["sinksmear"] = sinksmear

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)
