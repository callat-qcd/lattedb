# pylint: disable = E1101
"""Utility objects which help the unittests
"""
from typing import Dict, Any, List

from abc import ABC

from logging import getLogger

from espressodb.base.models import Base, ConsistencyError

LOGGER = getLogger("espressodb")


class ObjectParser(ABC):
    """Class which parses rescursive class creation arguments and runs creation tests.

    Todo:
        Include

        * Better description
        * Example
    """

    model: Base = None
    tree: Dict[str, Any] = {}
    parameters: Dict[str, Any] = {}
    consistency_check_changes: List[Dict[str, Any]] = []

    @classmethod
    def parse_args(cls, parameters: Dict[str, Any]):
        """Parses the argument tree of itself and dependencies
        """
        args = {}
        for key, val in parameters.items():
            if isinstance(val, dict):
                for kkey, vval in cls.parse_args(val).items():
                    args[f"{key}.{kkey}"] = vval
            else:
                args[key] = val
        return args

    def test_default_creation(self):
        """Tests if creation of model works with default entries.
        """
        pars = self.parse_args(self.parameters)
        LOGGER.debug(
            "Creating class %s with\n\tpars: %s\n\ttree: %s",
            self.model,
            pars,
            self.tree,
        )
        instance, created = self.model.get_or_create_from_parameters(
            self.parse_args(self.parameters), tree=self.tree
        )
        self.assertTrue(created)
        entries = self.model.objects.all()
        self.assertEqual(entries.count(), 1)
        self.assertEqual(entries.first(), instance)

    def test_inconsistent_creation(self):
        """Tests if creation of model works with default entries.
        """
        for parameter_updates in self.consistency_check_changes:
            pars = self.parse_args(self.parameters).copy()
            with self.subTest(**parameter_updates):
                pars.update(parameter_updates)
                LOGGER.debug(
                    "Creating class %s with\n\tpars: %s\n\ttree: %s",
                    self.model,
                    pars,
                    self.tree,
                )
                with self.assertRaises(ConsistencyError):
                    self.model.get_or_create_from_parameters(pars, tree=self.tree)
                entries = self.model.objects.all()
                self.assertEqual(entries.count(), 0)
