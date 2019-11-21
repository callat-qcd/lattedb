"""Tests for ensemble models
"""
from django.test import TestCase

from espressodb.base.models import ConsistencyError

from lattedb.utilities.tests import ObjectParser

from lattedb.ensemble.models import Ensemble
from lattedb.gaugeconfig.models import Nf211


class EnsembleTestCase(ObjectParser, TestCase):
    """Tests for EnsembleTestCase.
    """

    # Default test
    model = Ensemble
    tree = None
    parameters = {"label": "a01m134XXXXL"}
    consistency_check_changes = []

    def test_many_to_many(self):
        """Tests creation of many to many field which should not fail
        """
        ensemble = self.test_default_creation()

        gaugeconfig = Nf211(...)

        ensemble.configurations.add(gaugeconfig)
        ensemble.save()

        self.assertIn(gaugeconfig, Nf211.objects.filter(ensemble=ensemble))

    def test_many_to_many_consistency(self):
        """Tests creation of many to many field which should fail
        """
        ensemble = self.test_default_creation()

        gaugeconfig = Nf211(...)

        with self.assertRaises(ConsistencyError) as context:
            ensemble.configurations.add(gaugeconfig)
            ensemble.save()

        self.assertEqual(context.exception.message, "That was stupid...")
