"""Tests for ensemble models
"""
from django.test import TestCase

from espressodb.base.exceptions import ConsistencyError

from lattedb.utilities.tests import ObjectParser, BaseTest

from lattedb.ensemble.models import Ensemble
from lattedb.gaugeconfig.models import Nf211
from lattedb.gaugeconfig.tests import Nf211TParser


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

        gaugeconfig = Nf211TParser.create_instance()

        ensemble.configurations.add(gaugeconfig)
        ensemble.save()

        params = Nf211TParser.get_parameters()
        params["config"] = 1005
        gaugeconfig = Nf211TParser.create_instance(parameters=params)
        self.assertEqual(Nf211.objects.all().count(), 2)

        ensemble.configurations.add(gaugeconfig)

        self.assertIn(gaugeconfig, Nf211.objects.filter(ensemble=ensemble))

    def test_many_to_many_consistency(self):
        """Tests creation of many to many field which should fail
        """
        ensemble = Ensemble.objects.create(**self.parameters)

        gaugeconfig = Nf211TParser.create_instance()
        self.assertEqual(Nf211.objects.all().count(), 1)

        ensemble.configurations.add(gaugeconfig)

        params = Nf211TParser.get_parameters()
        params["config"] = 1005
        params["stream"] = "b"
        gaugeconfig = Nf211TParser.create_instance(parameters=params)

        self.assertEqual(Nf211.objects.all().count(), 2)

        with self.assertRaises(ConsistencyError) as context:
            ensemble.configurations.add(gaugeconfig)
        print(context.exception.error)
