"""Tests for ensemble models
"""
from django.test import TestCase

from espressodb.base.exceptions import ConsistencyError

from lattedb.utilities.tests import ObjectParser

from lattedb.ensemble.models import Ensemble
from lattedb.gaugeconfig.models import Nf211
from lattedb.gaugeconfig.tests import Nf211HisqParser


class EnsembleParser(ObjectParser):
    """Interface for quickly defining ensembles
    """

    # Default test
    model = Ensemble
    _tree = None
    _parameters = {"label": "a12m310a"}
    _consistency_check_changes = []


class EnsembleTestCase(EnsembleParser, TestCase):
    """Tests for EnsembleTestCase.
    """

    def test_many_to_many(self):
        """Tests creation of many to many field which should not fail
        """
        ensemble = Ensemble.objects.create(**self.parameters)

        gaugeconfig0 = Nf211HisqParser.create_instance()

        params = Nf211HisqParser.get_parameters()
        params["config"] = 1005
        gaugeconfig1 = Nf211HisqParser.create_instance(parameters=params)

        gaugeconfigs = [gaugeconfig0, gaugeconfig1]

        ensemble.configurations.add(*gaugeconfigs)

        parameters = {"label": "test"}
        ensemble = Ensemble.objects.create(**parameters)

        with self.assertRaises(ConsistencyError) as context:
            ensemble.configurations.add(*gaugeconfigs)
        print(context.exception.error)

    def test_gaugeconfig_id_consistency(self):
        """Tests creation of many to many field which should fail
        """
        ensemble = Ensemble.objects.create(**self.parameters)

        gaugeconfig = Nf211HisqParser.create_instance()
        self.assertEqual(Nf211.objects.all().count(), 1)

        ensemble.configurations.add(gaugeconfig)

        params = Nf211HisqParser.get_parameters()
        params["config"] = 1005
        params["stream"] = "b"
        gaugeconfig = Nf211HisqParser.create_instance(parameters=params)

        self.assertEqual(Nf211.objects.all().count(), 2)

        with self.assertRaises(ConsistencyError) as context:
            ensemble.configurations.add(gaugeconfig)
        print(context.exception.error)
