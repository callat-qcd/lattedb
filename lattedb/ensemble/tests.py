"""Tests for ensemble models
"""
from django.test import TestCase

from espressodb.base.exceptions import ConsistencyError

from lattedb.ensemble.models import Ensemble
from lattedb.gaugeconfig.models import Nf211
from lattedb.gaugeconfig import tests


class EnsembleTestCase(TestCase):
    """Tests for EnsembleTestCase.
    """

    # Default test
    model = Ensemble
    tree = None
    parameters = {"label": "a12m310a"}
    consistency_check_changes = []

    def test_many_to_many(self):
        """Tests creation of many to many field which should not fail
        """
        ensemble = Ensemble.objects.create(**self.parameters)

        nf211testcase = tests.Nf211TestCaseHisq()
        gaugeconfig = nf211testcase.test_default_creation()

        ensemble.configurations.add(gaugeconfig)
        ensemble.save()

        params = nf211testcase.parameters
        params["config"] = 1005
        nf211testcase.create_instance(parameters=params)
        self.assertEqual(Nf211.objects.all().count(), 2)

        ensemble.configurations.add(gaugeconfig)

        self.assertIn(gaugeconfig, Nf211.objects.filter(ensemble=ensemble))

    def test_many_to_many_consistency(self):
        """Tests creation of many to many field which should fail
        """
        ensemble = Ensemble.objects.create(**self.parameters)

        nf211testcase = tests.Nf211TestCaseHisq()
        gaugeconfig = nf211testcase.test_default_creation()
        self.assertEqual(Nf211.objects.all().count(), 1)

        ensemble.configurations.add(gaugeconfig)

        params = nf211testcase.parameters
        params["config"] = 1005
        params["stream"] = "b"
        gaugeconfig, _ = nf211testcase.create_instance(parameters=params)

        self.assertEqual(Nf211.objects.all().count(), 2)

        with self.assertRaises(ConsistencyError) as context:
            ensemble.configurations.add(gaugeconfig)
        print(context.exception.error)
