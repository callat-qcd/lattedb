"""Unittests for the correlator module
"""
from django.test import TestCase
from espressodb.base.exceptions import ConsistencyError

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.correlator.models import DWFTuning
from lattedb.propagator.tests import OneToAllDWssParser
from lattedb.propagator.tests import OneToAllHisqParser
from lattedb.wavefunction.tests import MesonParser


class DWFTuningParser(ObjectParser):
    """Tests creation of the Unsmeared link smear.
    """

    model = DWFTuning
    _tree = {
        "propagator": "OneToAll",
        **{
            f"propagator.{key}": OneToAllDWssParser.get_tree()[key]
            for key in OneToAllDWssParser.get_tree()
        },
        "wave": "Hadron",
    }
    _parameters = {
        "propagator": OneToAllDWssParser.get_parameters(),
        "wave": MesonParser.get_parameters(),
        "sink5": "False",
    }

    _consistency_check_changes = []


class DWFTuningBaseTest(DWFTuningParser, BaseTest, TestCase):
    ""


class DWFTuningTestCase(DWFTuningParser, TestCase):
    def test_propagator_type_consistency(self):
        """Write unittest when another fundamental propagator is defined
        """

    def test_fermionaction_type_consistency(self):
        """Test that fermion action is domain wall type
        """
        propagator = OneToAllHisqParser.create_instance()
        wave = MesonParser.create_instance()

        parameters = dict(self.get_parameters())
        parameters["propagator"] = propagator
        parameters["wave"] = wave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)


from lattedb.correlator.models import Meson2pt
from lattedb.propagator.tests import OneToAllDWParser


class Meson2ptParser(ObjectParser):
    """
    Test meson two point correlator table.
    The source and sink interpolating operators are not checked to be the same on purpose.
    """

    model = Meson2pt
    _tree = {
        "propagator0": "OneToAll",
        **{
            f"propagator0.{key}": OneToAllDWParser.get_tree()[key]
            for key in OneToAllDWParser.get_tree()
        },
        "propagator1": "OneToAll",
        **{
            f"propagator1.{key}": OneToAllDWParser.get_tree()[key]
            for key in OneToAllDWParser.get_tree()
        },
        "sourcewave": "Hadron",
        "sinkwave": "Hadron",
    }
    _parameters = {
        "propagator0": OneToAllDWssParser.get_parameters(),
        "propagator1": OneToAllDWssParser.get_parameters(),
        "sourcewave": MesonParser.get_parameters(),
        "sinkwave": MesonParser.get_parameters(),
    }
    _consistency_check_changes = []


class Meson2ptBaseTest(Meson2ptParser, BaseTest, TestCase):
    ""


class Meson2ptTestCase(Meson2ptParser, TestCase):
    def test_propagator_type_consistency(self):
        """
        Write this when a fundamental propagator type is defined.
        """

    def test_propagator_id_order_consistency(self):
        prop1 = OneToAllHisqParser.create_instance()
        prop0 = OneToAllDWssParser.create_instance()
        sourcewave = MesonParser.create_instance()
        sinkwave = MesonParser.create_instance(fail_if_exists=False)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_gaugeconfig_id_consistency(self):
        prop0 = OneToAllDWParser.create_instance()
        clsparameters = OneToAllDWParser.get_parameters()
        clstree = OneToAllDWParser.get_tree()
        clsparameters["gaugeconfig"]["config"] = (
            int(clsparameters["gaugeconfig"]["config"]) + 10
        )
        prop1 = OneToAllDWParser.create_instance(parameters=clsparameters, tree=clstree)
        sourcewave = MesonParser.create_instance()
        sinkwave = MesonParser.create_instance(fail_if_exists=False)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_sourcesmear_id_consistency(self):
        tree = dict(OneToAllDWssParser.get_tree())
        tree["sourcesmear"] = "Point"
        prop0 = OneToAllDWssParser.create_instance(tree=tree)
        prop1 = OneToAllDWssParser.create_instance()
        sourcewave = MesonParser.create_instance()
        sinkwave = MesonParser.create_instance(fail_if_exists=False)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_sinksmear_id_consistency(self):
        prop0 = OneToAllDWParser.create_instance()
        prop1 = OneToAllDWssParser.create_instance()
        sourcewave = MesonParser.create_instance()
        sinkwave = MesonParser.create_instance(fail_if_exists=False)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)


from lattedb.correlator.models import Baryon2pt
from lattedb.wavefunction.tests import HadronParser


class Baryon2ptParser(ObjectParser):
    model = Baryon2pt
    _tree = {
        "propagator0": "OneToAll",
        **{
            f"propagator0.{key}": OneToAllDWParser.get_tree()[key]
            for key in OneToAllDWParser.get_tree()
        },
        "propagator1": "OneToAll",
        **{
            f"propagator1.{key}": OneToAllDWParser.get_tree()[key]
            for key in OneToAllDWParser.get_tree()
        },
        "propagator2": "OneToAll",
        **{
            f"propagator2.{key}": OneToAllDWParser.get_tree()[key]
            for key in OneToAllDWParser.get_tree()
        },
        "sourcewave": "Hadron",
        "sinkwave": "Hadron",
    }
    _parameters = {
        "propagator0": OneToAllDWssParser.get_parameters(),
        "propagator1": OneToAllDWssParser.get_parameters(),
        "propagator2": OneToAllDWssParser.get_parameters(),
        "sourcewave": HadronParser.get_parameters(),
        "sinkwave": HadronParser.get_parameters(),
    }
    _consistency_check_changes = []


class Baryon2ptBaseTest(Baryon2ptParser, BaseTest, TestCase):
    ""


class Baryon2ptTestCase(Baryon2ptParser, TestCase):
    def test_propagator_type_consistency(self):
        """
        Write this when a fundamental propagator type is defined.
        """

    def test_propagator_id_order_consistency(self):
        prop1 = OneToAllHisqParser.create_instance()
        prop0 = OneToAllDWssParser.create_instance()
        prop2 = OneToAllDWssParser.create_instance(fail_if_exists=False)
        sourcewave = HadronParser.create_instance()
        sinkwave = HadronParser.create_instance(fail_if_exists=False)

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
        prop0 = OneToAllDWParser.create_instance()
        clsparameters = OneToAllDWParser.get_parameters()
        clstree = OneToAllDWParser.get_tree()
        clsparameters["gaugeconfig"]["config"] = (
            int(clsparameters["gaugeconfig"]["config"]) + 10
        )
        prop1 = OneToAllDWParser.create_instance(parameters=clsparameters, tree=clstree)
        prop2 = OneToAllDWParser.create_instance(fail_if_exists=False)
        sourcewave = MesonParser.create_instance()
        sinkwave = MesonParser.create_instance(fail_if_exists=False)

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
        tree = dict(OneToAllDWssParser.get_tree())
        tree["sourcesmear"] = "Point"
        prop0 = OneToAllDWssParser.create_instance(tree=tree)
        prop1 = OneToAllDWssParser.create_instance()
        prop2 = OneToAllDWssParser.create_instance(fail_if_exists=False)
        sourcewave = MesonParser.create_instance()
        sinkwave = MesonParser.create_instance(fail_if_exists=False)

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
        prop0 = OneToAllDWParser.create_instance()
        prop1 = OneToAllDWssParser.create_instance()
        prop2 = OneToAllDWssParser.create_instance(fail_if_exists=False)
        sourcewave = MesonParser.create_instance()
        sinkwave = MesonParser.create_instance(fail_if_exists=False)

        parameters = dict()
        parameters["propagator0"] = prop0
        parameters["propagator1"] = prop1
        parameters["propagator2"] = prop2
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)


from lattedb.correlator.models import BaryonSeq3pt
from lattedb.current.tests import LocalParser
from lattedb.propagator.tests import BaryonCoherentSeqParser
from lattedb.quarksmear.tests import PointParser


class BaryonSeq3ptParser(ObjectParser):
    model = BaryonSeq3pt
    _tree = {
        "sourcewave": "Hadron",
        "current": "Local",
        "seqpropagator": "BaryonCoherentSeq",
        **{
            f"seqpropagator.{key}": BaryonCoherentSeqParser.get_tree()[key]
            for key in BaryonCoherentSeqParser.get_tree()
        },
        "propagator": "OneToAll",
        **{
            f"propagator.{key}": OneToAllDWParser.get_tree()[key]
            for key in OneToAllDWParser.get_tree()
        },
    }
    _parameters = {
        "sourcewave": HadronParser.get_parameters(),
        "current": LocalParser.get_parameters(),
        "seqpropagator": BaryonCoherentSeqParser.get_parameters(),
        "propagator": OneToAllDWParser.get_parameters(),
    }

    _consistency_check_changes = []

    @classmethod
    def create_populated_instance(cls):
        """
        """
        # black magic makes this run first (class inheritance)
        baryoncoherentseq = BaryonCoherentSeqParser.create_populated_instance()
        sourcewave = HadronParser.create_instance(fail_if_exists=False)
        current = LocalParser.create_instance()
        propagator = OneToAllDWssParser.create_instance()

        parameters = dict()
        parameters["sourcewave"] = sourcewave
        parameters["current"] = current
        parameters["seqpropagator"] = baryoncoherentseq
        parameters["propagator"] = propagator

        return cls.model.objects.create(**parameters)


class BaryonSeq3ptTestCase(BaryonSeq3ptParser, TestCase):
    def test_default_creation(self):
        self.create_populated_instance()

    def test_sinksmear_id_consistency(self):
        sourcewave = HadronParser.create_instance()
        current = LocalParser.create_instance()
        seqpropagator = self.baryoncoherentseq
        propagator = OneToAllDWssParser.create_instance()

        parameters = dict()
        parameters["sourcewave"] = sourcewave
        parameters["current"] = current
        parameters["seqpropagator"] = seqpropagator
        parameters["propagator"] = propagator

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def test_sourcesmear_id_consistency(self):
        sourcewave = HadronParser.create_instance()
        current = LocalParser.create_instance()
        seqpropagator = self.baryoncoherentseq
        onetoalltestcase = OneToAllDWParser()
        onetoallparameters = dict(onetoalltestcase.get_parameters())
        onetoallparameters["sourcesmear"] = PointParser.create_instance()
        tree = onetoalltestcase.get_tree()
        tree["sourcesmear"] = "Point"
        propagator = onetoalltestcase.create_instance(
            parameters=onetoallparameters, tree=onetoalltestcase.get_tree()
        )
        parameters = dict()
        parameters["sourcewave"] = sourcewave
        parameters["current"] = current
        parameters["seqpropagator"] = seqpropagator
        parameters["propagator"] = propagator

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def check_origin_consistency(self):
        sourcewave = HadronParser.create_instance()
        current = LocalParser.create_instance()
        seqpropagator = self.baryoncoherentseq
        onetoalltestcase = OneToAllDWParser()
        onetoallparameters = dict(onetoalltestcase.get_parameters())
        onetoallparameters["origin_x"] = int(onetoallparameters["origin_x"]) + 5
        propagator = onetoalltestcase.create_instance(
            parameters=onetoallparameters, tree=onetoalltestcase.get_tree()
        )
        parameters = dict()
        parameters["sourcewave"] = sourcewave
        parameters["current"] = current
        parameters["seqpropagator"] = seqpropagator
        parameters["propagator"] = propagator

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)


from lattedb.correlator.models import BaryonFH3pt
from lattedb.propagator.tests import FeynmanHellmannParser


class BaryonFH3ptParser(ObjectParser):
    model = BaryonFH3pt
    _tree = {
        "sourcewave": "Hadron",
        "sinkwave": "Hadron",
        "fhpropagator": "FeynmanHellmann",
        **{
            f"fhpropagator.{key}": FeynmanHellmannParser.get_tree()[key]
            for key in FeynmanHellmannParser.get_tree()
        },
        "propagator0": "OneToAll",
        **{
            f"propagator0.{key}": OneToAllDWParser.get_tree()[key]
            for key in OneToAllDWParser.get_tree()
        },
        "propagator1": "OneToAll",
        **{
            f"propagator1.{key}": OneToAllDWParser.get_tree()[key]
            for key in OneToAllDWParser.get_tree()
        },
    }
    _parameters = {
        "sourcewave": HadronParser.get_parameters(),
        "sinkwave": HadronParser.get_parameters(),
        "fhpropagator": FeynmanHellmannParser.get_parameters(),
        "propagator0": OneToAllDWParser.get_parameters(),
        "propagator1": OneToAllDWParser.get_parameters(),
    }
    _consistency_check_changes = []


class BaryonFH3ptBaseTest(BaryonFH3ptParser, BaseTest, TestCase):
    ""


class BaryonFH3ptTestCase(BaryonFH3ptParser, TestCase):
    def check_propagator_id_order_consistency(self):
        sourcewave = HadronParser.create_instance()
        sinkwave = HadronParser.create_instance(fail_if_exists=False)
        fhpropagator = FeynmanHellmannParser.create_instance()
        propagator1 = OneToAllDWParser.create_instance()
        onetoalltestcase = OneToAllDWParser()
        onetoallparameters = dict(onetoalltestcase.get_parameters())
        onetoallparameters["fermionaction"]["quark_mass"] = 0.2
        onetoallparameters["fermionaction"]["quark_tag"] = "strange"
        propagator0 = onetoalltestcase.create_instance(
            parameters=onetoallparameters, tree=onetoalltestcase.get_tree()
        )
        parameters = dict()
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave
        parameters["fhpropagator"] = fhpropagator
        parameters["propagator0"] = propagator0
        parameters["propagator1"] = propagator1

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def check_sourcesmear_id_consistency(self):
        sourcewave = HadronParser.create_instance()
        sinkwave = HadronParser.create_instance(fail_if_exists=False)
        fhpropagator = FeynmanHellmannParser.create_instance()
        propagator0 = OneToAllDWParser.create_instance()
        onetoalltestcase = OneToAllDWParser()
        onetoallparameters = dict(onetoalltestcase.get_parameters())
        onetoallparameters["sourcesmear"] = PointParser.create_instance()
        tree = onetoalltestcase.get_tree()
        tree["sourcesmear"] = "Point"
        propagator1 = onetoalltestcase.create_instance(
            parameters=onetoallparameters, tree=onetoalltestcase.get_tree()
        )

        parameters = dict()
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave
        parameters["fhpropagator"] = fhpropagator
        parameters["propagator0"] = propagator0
        parameters["propagator1"] = propagator1

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)

    def check_sinksmear_id_consistency(self):
        sourcewave = HadronParser.create_instance()
        sinkwave = HadronParser.create_instance(fail_if_exists=False)
        fhpropagator = FeynmanHellmannParser.create_instance()
        propagator0 = OneToAllDWParser.create_instance()
        propagator1 = OneToAllDWssParser.create_instance()

        parameters = dict()
        parameters["sourcewave"] = sourcewave
        parameters["sinkwave"] = sinkwave
        parameters["fhpropagator"] = fhpropagator
        parameters["propagator0"] = propagator0
        parameters["propagator1"] = propagator1

        with self.assertRaises(ConsistencyError) as context:
            self.model.objects.create(**parameters)
        print(context.exception.error)
