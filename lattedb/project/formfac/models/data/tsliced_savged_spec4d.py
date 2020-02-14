# pylint: disable=E1101
"""Models of time sliced and source averaged spectrum 4D files.
"""
from django.db import models
from lattedb.project.formfac.models.data import (
    AbstractSpectrum4DFile,
    PhysicalSpectrum4DFile,
)


class TSlicedSAveragedSpectrum4DFile(AbstractSpectrum4DFile):
    """Table storing information about time sliced and source averaged spectrum files.

    This is not the "physical" file information but rather the meta info.
    """

    verbose_name = " TSliced Source Averaged Spectrum 4D File"

    configuration = models.IntegerField(help_text="Number of configuration.")

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = [
            "ensemble",
            "stream",
            "source_set",
            "configuration",
        ]


class TapeTSlicedSAveragedSpectrum4DFile(PhysicalSpectrum4DFile):
    """Table associates time sliced and source averaged spectrum file meta information
    with a physical file on tape.
    """

    verbose_name = " TSliced Source Averaged Spectrum 4D File on Tape"

    file = models.OneToOneField(
        TSlicedSAveragedSpectrum4DFile,
        on_delete=models.CASCADE,
        related_name="tape",
        help_text="The file meta information.",
    )


class DiskTSlicedSAveragedSpectrum4DFile(PhysicalSpectrum4DFile):
    """Table associates time sliced and source averaged form factor file meta information
    with a physical file on disk.
    """

    verbose_name = " TSliced Source Averaged Spectrum 4D File on Disk"

    file = models.OneToOneField(
        TSlicedSAveragedSpectrum4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
