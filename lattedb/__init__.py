# pylint: disable=C0413
"""Easy access to models
"""
import os
from django import setup as _setup


def _init():
    """Initializes the django environment for my_project
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lattedb.config.settings")
    _setup()


_init()
