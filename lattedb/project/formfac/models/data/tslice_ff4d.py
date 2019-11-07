"""Models of time sliced form factor 4D files.
"""
from django.db import models
from lattedb.project.formfac.models.data import (
    AbstractFormFactor4DFile,
    PhysicalFormFactor4DFile,
)


class TSlicedFormFactor4DFile(AbstractFormFactor4DFile):
    """Table storing information about time sliced form factor files.

    This is not the "physical" file information but rather the meta info.
    """

    configuration = models.IntegerField(help_text="Number of configuration.")
    t_separation = models.IntegerField(help_text="Source sink separation.")
    source = models.CharField(
        max_length=100, help_text="Source location in format `xXyYzZtT`."
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = [
            "ensemble",
            "stream",
            "source_set",
            "current",
            "state",
            "parity",
            "flavor",
            "spin",
            "configuration",
            "t_separation",
            "source",
        ]


class DiskTSlicedFormFactor4DFile(PhysicalFormFactor4DFile):
    """Table associates time sliced form factor file meta information with a physical
    file on disk.
    """

    file = models.ForeignKey(
        TSlicedFormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
