"""Correlator file status tables

ToDo:
    * Agree on naming convention
    * Updated allowed type choices for CorrelatorStatus
"""
from os.path import join

from h5py import File

from django.db import models
from espressodb.base.models import Base


class AbstractH5Dset(Base):
    """Table for physical file information summarizing disk or tape h5 file status.
    """

    name = models.TextField(help_text="The name of the file.")
    path = models.TextField(help_text="The directory path of the file.")
    dset = models.TextField(help_text="The path to the dset.")
    exists = models.BooleanField(
        null=False,
        help_text="Can the file be found at"
        " `physical_file.path/physical_file.file.name/dset_path`?.",
    )
    machine = models.CharField(
        max_length=100, help_text="The machine the file can be found on."
    )
    date_modified = models.DateTimeField(
        null=True, help_text="The last time the file was modified."
    )

    class Meta:  # pylint: disable=C0111, R0903
        abstract = True

    @classmethod
    def get_doc(cls) -> str:
        """Returns the doc string
        """
        return cls.__doc__

    @property
    def file_address(self) -> str:
        """The address to the file.
        """
        return join(self.path, self.name)


TYPE_CHOICES = [
    (
        "res_phi_ll",
        "Residual quark mass and connected pion-like meson correlators for quark mass m_l",
    ),
    (
        "res_phi_ss",
        "Residual quark mass and connected pion-like meson correlators for quark mass m_s",
    ),
    ("spec", "Pi+, proton, proton np"),
    ("ff", "Form Factor of proton for MANY currents"),
    ("h_spec", "Hyperon Spectrum"),
]


class CorrelatorMeta(Base):
    """Correlator file meta information table.

    Options for `correlator` are:

    `"res_phi_ll"`: Residual quark mass and connected
        pion-like meson correlators for quark mass m_l;
    `"res_phi_ss"`: Residual quark mass and connected
        pion-like meson correlators for quark mass m_s;
    `"spec"`: Pi+, proton, proton np;
    `"ff"`: Form Factor of proton for MANY currents;
    `"h_spec"`: Hyperon Spectrum.
    """

    correlator = models.CharField(
        max_length=20, choices=TYPE_CHOICES, help_text="Type of the correlator."
    )
    ensemble = models.CharField(
        max_length=100, help_text="Name of the ensemble. E.g., `a15m135XL`."
    )
    stream = models.CharField(
        max_length=10, help_text="Name of the HMC stream, e.g., `a`."
    )
    configuration = models.IntegerField(help_text="Configuration number.")
    source_set = models.CharField(
        max_length=100, help_text="Set of sources in this file. E.g., `16-23`."
    )
    source = models.CharField(
        max_length=20, help_text="Source location (e.g., `xXyYzZtT`)."
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = [
            "correlator",
            "ensemble",
            "stream",
            "configuration",
            "source_set",
            "source",
        ]

    @classmethod
    def get_doc(cls) -> str:
        """Returns the doc string
        """
        return cls.__doc__


class DiskCorrelatorH5Dset(AbstractH5Dset):
    """Correlator h5dset on Disk information
    """

    verbose_name = "Correlator h5dset on Disk"

    meta = models.OneToOneField(
        CorrelatorMeta,
        on_delete=models.CASCADE,
        related_name="disk",
        help_text="The file meta information.",
    )

    @property
    def data(self) -> "array":
        """Accesses dset in read mode from stored location
        """
        with File(self.file_address, "r") as inp:
            data = inp[self.dset][:]
        return data


class TapeCorrelatorH5Dset(AbstractH5Dset):
    """Correlator h5dset on tape information
    """

    verbose_name = "Correlator h5dset on Tape"

    meta = models.OneToOneField(
        CorrelatorMeta,
        on_delete=models.CASCADE,
        related_name="tape",
        help_text="The file meta information.",
    )
