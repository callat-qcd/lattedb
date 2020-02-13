"""Models of time sliced spectrum 4D files.
"""
from django.db import models

from lattedb.project.formfac.models.data import (
    AbstractSpectrum4DFile,
    PhysicalSpectrum4DFile,
)
from lattedb.project.formfac.models.data.tsliced_savged_spec4d import (
    TSlicedSAveragedSpectrum4DFile,
)


class TSlicedSpectrum4DFile(AbstractSpectrum4DFile):
    """Table storing information about time sliced spectrum files.

    This is not the "physical" file information but rather the meta info.
    """

    verbose_name = " TSliced Spectrum 4D File"

    configuration = models.IntegerField(help_text="Number of configuration.")
    source = models.CharField(
        max_length=100, help_text="Source location in format `xXyYzZtT`."
    )
    dependent = models.ForeignKey(
        TSlicedSAveragedSpectrum4DFile,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Link to t-sliced source averaged spectrum file.",
        related_name="dependencies",
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = [
            "ensemble",
            "stream",
            "source_set",
            "configuration",
            "source",
        ]


class DiskTSlicedSpectrum4DFile(PhysicalSpectrum4DFile):
    """Table associates time sliced spectrum file meta information with a physical
    file on disk.
    """

    verbose_name = " TSliced Spectrum 4D File on Disk"

    file = models.OneToOneField(
        TSlicedSpectrum4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
