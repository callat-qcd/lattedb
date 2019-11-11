# pylint: disable=E1101
"""Models of time sliced and source averaged form factor 4D files.
"""
from typing import List
from django.db import models
from lattedb.project.formfac.models.data import (
    AbstractFormFactor4DFile,
    PhysicalFormFactor4DFile,
)


class TSlicedSAveragedFormFactor4DFile(AbstractFormFactor4DFile):
    """Table storing information about time sliced and source averaged form factor files.

    This is not the "physical" file information but rather the meta info.
    """

    verbose_name = " TSliced Source Averaged Form Factor 4D File"

    configuration = models.IntegerField(help_text="Number of configuration.")
    t_separation = models.IntegerField(help_text="Source sink time separation.")

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = [
            "ensemble",
            "stream",
            "source_set",
            "configuration",
            "t_separation",
        ]


class TapeTSlicedSAveragedFormFactor4DFile(PhysicalFormFactor4DFile):
    """Table associates time sliced and source averaged form factor file meta information
    with a physical file on tape.
    """

    verbose_name = " TSliced Source Averaged Form Factor 4D File on Tape"

    file = models.OneToOneField(
        TSlicedSAveragedFormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="tape",
        help_text="The file meta information.",
    )


class DiskTSlicedSAveragedFormFactor4DFile(PhysicalFormFactor4DFile):
    """Table associates time sliced and source averaged form factor file meta information
    with a physical file on disk.
    """

    verbose_name = " TSliced Source Averaged Form Factor 4D File on Disk"

    file = models.OneToOneField(
        TSlicedSAveragedFormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )

    @property
    def n_sources(self):
        """Computes the number of sources from the source string.
        """
        n_min, n_max = self.file.source_set.replace("-", "")
        return int(n_max) - int(n_min) + 1

    @property
    def dependencies_exist(self) -> bool:
        """Check wether dependent t-sliced form factor 4D files exists on disk

        Files don't exist if:
            1. The number of dependencies is not equal to the number of sources in the
               group
            2. The disk status of any dependency is not True
        """
        exist = False
        if self.file.dependencies.count() == self.n_sources:
            if all(self.file.dependencies.values_list("disk__exists")):
                exist = True
        return exist

    @classmethod
    def get_missing_files(cls) -> List["DiskTSlicedSAveragedFormFactor4DFile"]:
        """Get all DiskTSlicedSAveragedFormFactor4DFile which don't exist.
        """
        cls.objects.filter(exists=False)

    @classmethod
    def get_files_with_missing_dependencies(
        cls, expected_dependencies: int = 8
    ) -> List["DiskTSlicedSAveragedFormFactor4DFile"]:
        """Get all DiskTSlicedSAveragedFormFactor4DFile where the dependency does not
        exist.

        Note:
            Currently expected_dependencies to exist is hardcoded.

        Dependency does not exists is defined by:
            1. Not expected_dependencies dependency files are in the db,
            2. No file status is associated with the dependency file,
            3. The file status of the dependency file is does not exist.
        """
        return cls.objects.annotate(models.Count("file__dependencies")).filter(
            models.Q(file__dependencies__count__ne=expected_dependencies)
            | models.Q(file__dependencies__disk__isnull=True)
            | models.Q(file__dependencies__disk__exists=False)
        )
