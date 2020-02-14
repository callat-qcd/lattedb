"""Abstract help tables for 4D Form Factor and Spectrum tables
"""
from os.path import join

from django.db import models
from espressodb.base.models import Base


class AbstractFormFactor4DFile(Base):
    """Abstract form factor 4D file table.

    All specialized tables like FormFactor4D with tslice, src_avg, ... should inherit
    from this table.
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
    source_set = models.CharField(
        max_length=100, help_text="Set of sources in this file. E.g., `16-23`."
    )

    class Meta:  # pylint: disable=C0111, R0903
        abstract = True

    @classmethod
    def get_doc(cls) -> str:
        """Returns the doc string
        """
        return cls.__doc__


class AbstractSpectrum4DFile(Base):
    """Abstract form factor 4D file table.

    All specialized tables like FormFactor4D with tslice, src_avg, ... should inherit
    from this table.
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
    source_set = models.CharField(
        max_length=100, help_text="Set of sources in this file. E.g., `16-23`."
    )

    class Meta:  # pylint: disable=C0111, R0903
        abstract = True

    @classmethod
    def get_doc(cls) -> str:
        """Returns the doc string
        """
        return cls.__doc__


class PhysicalFormFactor4DFile(Base):
    """Abstract table for physical file information summarizing disk or file status.
    """

    file = models.OneToOneField(
        AbstractFormFactor4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
    path = models.TextField(help_text="The directory path.")
    exists = models.BooleanField(
        null=False,
        help_text="Can the file be found `physical_file.path/physical_file.file.name`?.",
    )
    machine = models.CharField(
        max_length=100, help_text="The machine the file can be found on."
    )
    size = models.BigIntegerField(null=True, help_text="Size of the file in Bytes.")
    date_modified = models.DateTimeField(
        null=True, help_text="The last time the file was modified."
    )

    class Meta:  # pylint: disable=C0111, R0903
        abstract = True

    @property
    def filepath(self) -> str:
        """The actual path to the file.
        """
        return join(self.path, self.file.name)

    @classmethod
    def get_doc(cls) -> str:
        """Returns the doc string
        """
        return cls.__doc__


class PhysicalSpectrum4DFile(Base):
    """Abstract table for physical file information summarizing disk or file status.
    """

    file = models.OneToOneField(
        AbstractSpectrum4DFile,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )
    path = models.TextField(help_text="The directory path.")
    exists = models.BooleanField(
        null=False,
        help_text="Can the file be found `physical_file.path/physical_file.file.name`?.",
    )
    machine = models.CharField(
        max_length=100, help_text="The machine the file can be found on."
    )
    size = models.BigIntegerField(null=True, help_text="Size of the file in Bytes.")
    date_modified = models.DateTimeField(
        null=True, help_text="The last time the file was modified."
    )

    class Meta:  # pylint: disable=C0111, R0903
        abstract = True

    @property
    def filepath(self) -> str:
        """The actual path to the file.
        """
        return join(self.path, self.file.name)

    @classmethod
    def get_doc(cls) -> str:
        """Returns the doc string
        """
        return cls.__doc__
