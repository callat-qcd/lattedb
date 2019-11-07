"""Models of concatenated form factor 4D files.
"""
from django.db import models
from lattedb.project.formfac.models.data import (
    AbstractFormFactor4DFile,
    PhysicalFormFactor4DFile,
)


class ConcatenatedFormFactor4DFile(AbstractFormFactor4DFile):
    """Table storing information about concatenated source averated and time sliced
    form factor files.

    This is not the "physical" file information but rather the meta info.
    """

    current = models.CharField(
        max_length=20, help_text="Name of the current. E.g., `V2`."
    )
    state = models.CharField(
        max_length=100, help_text="Name of the state. E.g., `proton`."
    )
    parity = models.IntegerField(help_text="Parity of the state. E.g., + or -1.")
    flavor = models.CharField(
        max_length=20, help_text="Flavor of the state. E.g., `UU`."
    )
    spin = models.CharField(
        max_length=20, help_text="Spin of the state. E.g., `up_up`."
    )
    configuration_range = models.CharField(
        max_length=100,
        help_text="Range of configuration in this file. E.g., `500-1745`.",
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = [
            "ensemble",
            "stream",
            "configuration_range",
            "source_set",
            "current",
            "state",
            "parity",
            "flavor",
            "spin",
        ]


class TapeConcatenatedFormFactor4DFile(PhysicalFormFactor4DFile):
    """Table associates concatenated source averated and time sliced form factor file
    meta information with a physical file on tape.
    """

    file = models.ForeignKey(
        ConcatenatedFormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="tape",
        help_text="The file meta information.",
    )


class DiskConcatenatedFormFactor4DFile(PhysicalFormFactor4DFile):
    """Table associates concatenated source averated and time sliced form factor file
    meta information with a physical file on disk.
    """

    file = models.ForeignKey(
        ConcatenatedFormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
