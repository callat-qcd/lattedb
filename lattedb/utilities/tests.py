# pylint: disable = E1101
"""Utility objects which help the unittests
"""
from typing import Dict, Any, List, Optional

from abc import ABC

from logging import getLogger


from espressodb.base.models import Base
from espressodb.base.exceptions import ConsistencyError

LOGGER = getLogger("espressodb")


class ObjectParser(ABC):
    """Class which parses rescursive class creation arguments and runs creation tests.

    Todo:
        Include

        * Better description
        * Example
    """

    model: Base = None
    _tree: Dict[str, Any] = {}
    _parameters: Dict[str, Any] = {}
    _consistency_check_changes: List[Dict[str, Any]] = []

    @classmethod
    def get_tree(cls):
        """Returns a copy of the class tree
        """
        return cls._tree.copy() if cls._tree else {}

    @classmethod
    def get_parameters(cls):
        """Returns a copy of the class parameters
        """
        return cls._parameters.copy() if cls._parameters else {}

    @classmethod
    def get_consistency_check_changes(cls):
        """Returns a copy of the class consistency check changes
        """
        return (
            cls._consistency_check_changes.copy()
            if cls._consistency_check_changes
            else []
        )

    @property
    def tree(self):
        """Returns a copy of the class tree
        """
        return self.get_tree()

    @property
    def parameters(self):
        """Returns a copy of the class parameters
        """
        return self.get_parameters()

    @property
    def consistency_check_changes(self):
        """Returns a copy of the class consistency check changes
        """
        return self.get_consistency_check_changes()

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

    @classmethod
    def create_instance(
        cls,
        parameters: Optional[Dict[str, Any]] = None,
        tree: Optional[Dict[str, Any]] = None,
        fail_if_exists: bool = True,
    ) -> Base:
        """Creates a instance of the class.

         Arguments:
            parameters:
                Parameters used to construct the whole tree. Defaults to
                `self.parameters`.
            tree:
                Tree (nsted dependencies) used to construct the class. Defaults to
                `self.tree`.
            fail_if_exists:
                Raise Key error if flag is true and instance already existed in db.

        Returns:
            The instance and a bool if it was created or not.
        """
        pars = cls.parse_args(parameters or cls.get_parameters())
        tree = tree or cls.get_tree()
        LOGGER.debug(
            "Creating class %s with\n\tpars: %s\n\ttree: %s", cls.model, pars, tree,
        )
        instance, created = cls.model.get_or_create_from_parameters(pars, tree=tree)

        if not created and fail_if_exists:
            raise AssertionError(f"Instance {instance} already exist in db")

        return instance


class BaseTest(ABC):
    """Class which runs default creation tests

    Todo:
        Include

        * Better description
        * Example
    """

    def test_default_creation(
        self,
        parameters: Optional[Dict[str, Any]] = None,
        tree: Optional[Dict[str, Any]] = None,
    ) -> Base:
        """Tests if creation of model works with default entries.

        Arguments:
            parameters:
                Parameters used to construct the whole tree. Defaults to
                `self.parameters`.
            tree:
                Tree (nsted dependencies) used to construct the class. Defaults to
                `self.tree`.
        """
        instance = self.create_instance(parameters, tree=tree, fail_if_exists=True)
        entries = self.model.objects.all()
        self.assertEqual(entries.count(), 1)
        self.assertEqual(entries.first(), instance)

        return instance

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
