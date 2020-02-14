"""Models of spectrum 4D files.
"""
from django.db import models
from lattedb.project.formfac.models.data import (
    AbstractSpectrum4DFile,
    PhysicalSpectrum4DFile,
)
from lattedb.project.formfac.models.data.tsliced_spec4d import TSlicedSpectrum4DFile


class Spectrum4DFile(AbstractSpectrum4DFile):
    """Table storing information about spectrum files.

    This is not the "physical" file information but rather the meta info.
    """

    verbose_name = "Spectrum4D File"

    configuration = models.IntegerField(help_text="Number of configuration.")
    source = models.CharField(
        max_length=100, help_text="Source location in format `xXyYzZtT`."
    )
    dependent = models.OneToOneField(
        TSlicedSpectrum4DFile,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Link to t-sliced spectrum file.",
        related_name="dependency",
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = [
            "ensemble",
            "stream",
            "source_set",
            "configuration",
            "source",
        ]


class DiskSpectrum4DFile(PhysicalSpectrum4DFile):
    """Table associates spectrum file meta information with a physical file on disk.
    """

    verbose_name = "Spectrum4D File on Disk"

    file = models.OneToOneField(
        Spectrum4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
