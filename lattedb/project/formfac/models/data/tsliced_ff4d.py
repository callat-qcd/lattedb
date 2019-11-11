"""Models of time sliced form factor 4D files.
"""
from typing import List

from django.db import models

from lattedb.project.formfac.models.data import (
    AbstractFormFactor4DFile,
    PhysicalFormFactor4DFile,
)
from lattedb.project.formfac.models.data.tsliced_savged_ff4d import (
    TSlicedSAveragedFormFactor4DFile,
)


class TSlicedFormFactor4DFile(AbstractFormFactor4DFile):
    """Table storing information about time sliced form factor files.

    This is not the "physical" file information but rather the meta info.
    """

    verbose_name = " TSliced Form Factor 4D File"

    configuration = models.IntegerField(help_text="Number of configuration.")
    t_separation = models.IntegerField(help_text="Source sink time separation.")
    source = models.CharField(
        max_length=100, help_text="Source location in format `xXyYzZtT`."
    )
    dependent = models.ForeignKey(
        TSlicedSAveragedFormFactor4DFile,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Link to t-sliced source averaged form factor file.",
        related_name="dependencies",
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = [
            "ensemble",
            "stream",
            "source_set",
            "configuration",
            "t_separation",
            "source",
        ]


class DiskTSlicedFormFactor4DFile(PhysicalFormFactor4DFile):
    """Table associates time sliced form factor file meta information with a physical
    file on disk.
    """

    verbose_name = " TSliced Form Factor 4D File on Disk"

    file = models.ForeignKey(
        TSlicedFormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )

    @property
    def dependency_exists(self) -> bool:
        """Check wether dependent form factor 4D file exists on disk
        """
        return self.file.dependency.disk.exists  # pylint: disable=E1101

    @classmethod
    def get_missing_files(cls) -> List["DiskTSlicedFormFactor4DFile"]:
        """Get all DiskTSlicedFormFactor4DFile which don't exist.
        """
        cls.objects.filter(exists=False)

    @classmethod
    def get_files_with_missing_dependencies(cls) -> List["DiskTSlicedFormFactor4DFile"]:
        """Get all DiskTSlicedFormFactor4DFile where the dependency does not exist.

        Dependency does not exists is defined by:
            1. No dependency file is in the db,
            2. No file status is associated with the dependency file,
            3. The file status of the dependency file is does not exist.
        """
        return cls.objects.filter(
            models.Q(file__dependency__isnull=True)
            | models.Q(file__dependency__disk__isnull=True)
            | models.Q(file__dependency__disk__exists=False)
        )
