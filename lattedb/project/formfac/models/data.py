"""Models of formfac
"""
from os.path import join

from django.db import models
from espressodb.base.models import Base


class FormFactor4DFile(Base):
    """Table storing information about form factor files.

    This is not the "physical" file information but rather the meta info.
    """

    name = models.TextField(
        unique=True, help_text="Name of the file. Should not include folders."
    )
    ensemble = models.CharField(
        max_length=100, help_text="Name of the ensemble. E.g., `a15m135XL`."
    )
    stream = models.CharField(
        max_length=10, help_text="Name of the HMC stream, e.g., `a`."
    )
    configuration_range = models.CharField(
        max_length=100,
        help_text="Range of configuration in this file. E.g., `500-1745`.",
    )
    source_set = models.CharField(
        max_length=100, help_text="Set of sources in this file. E.g., `16-23`."
    )
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


class TapeFormFactor4DFile(Base):
    """Table associates Form Factor file meta information with a physical file on tape.
    """

    file = models.ForeignKey(
        FormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="tape",
        help_text="The file meta information.",
    )
    path = models.TextField(help_text="The directory path on tape.")
    exits = models.BooleanField(
        null=False,
        help_text="Can the file be found `tape_file.path/tape_file.file.name`?.",
    )
    machine = models.CharField(
        max_length=100, help_text="The machine the file can be found on."
    )
    size = models.IntegerField(null=True, help_text="Size of the file in Bytes.")
    date_modified = models.DateTimeField(
        null=True, help_text="The last time the file was modified."
    )

    @property
    def filepath(self) -> str:
        """The actual path to the file.
        """
        return join(self.path, self.file.name)


class DiskFormFactor4DFile(Base):
    """Table associates Form Factor file meta information with a physical file on disk.
    """

    file = models.ForeignKey(
        FormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
    path = models.TextField(help_text="The directory path on disk.")
    exits = models.BooleanField(
        null=False,
        help_text="Can the file be found `disk_file.path/disk_file.file.name`?.",
    )
    machine = models.CharField(
        max_length=100, help_text="The machine the file can be found on."
    )
    size = models.IntegerField(null=True, help_text="Size of the file in Bytes.")
    date_modified = models.DateTimeField(
        null=True, help_text="The last time the file was modified."
    )

    @property
    def filepath(self) -> str:
        """The actual path to the file.
        """
        return join(self.path, self.file.name)
