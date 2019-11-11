"""Models ofform factor 4D files.
"""
from django.db import models
from lattedb.project.formfac.models.data import (
    AbstractFormFactor4DFile,
    PhysicalFormFactor4DFile,
)
from lattedb.project.formfac.models.data.tsliced_ff4d import TSlicedFormFactor4DFile


class FormFactor4DFile(AbstractFormFactor4DFile):
    """Table storing information about form factor files.

    This is not the "physical" file information but rather the meta info.
    """

    verbose_name = "FormFactor4D File"

    configuration = models.IntegerField(help_text="Number of configuration.")
    t_separation = models.IntegerField(help_text="Source sink time separation.")
    source = models.CharField(
        max_length=100, help_text="Source location in format `xXyYzZtT`."
    )
    dependent = models.OneToOneField(
        TSlicedFormFactor4DFile,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Link to t-sliced form factor file.",
        related_name="dependency",
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


class DiskFormFactor4DFile(PhysicalFormFactor4DFile):
    """Table associates form factor file meta information with a physical file on disk.
    """

    verbose_name = "FormFactor4D File on Disk"

    file = models.OneToOneField(
        FormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
