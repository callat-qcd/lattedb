from typing import Dict, Any
from django.db import models

from espressodb.base.models import Base


class SCSWaveFunction(Base):
    r"""
    Base table for application.
    All types of interpolating operators are listed here.
    If applicable, consistency is enforced in check_consistency under each table that references `wavefunction.scswavefunction`.
    """


class Hadron4D(SCSWaveFunction):
    r"""
    Hadronic interpolating operators.
    No momentum projection is performed here.
    The entries should have counterparts at `wavefunction.hadron`.
    Reference to Basak operators: https://arxiv.org/abs/hep-lat/0508018.
    """

    description = models.TextField(
        null=True, blank=True, help_text="Description of the interpolating operator"
    )
    strangeness = models.PositiveSmallIntegerField(
        null=False, help_text="Strangeness of hadronic operator"
    )
    irrep = models.TextField(
        null=False,
        blank=False,
        help_text="Irreducible representations of O^D_h (octahedral group)",
    )
    embedding = models.PositiveSmallIntegerField(
        null=False, blank=False, help_text="k-th embedding of O^D_h irrep."
    )

    parity = models.SmallIntegerField(
        null=False, help_text="Parity of hadronic operator"
    )
    spin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Total spin times 2"
    )

    spin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Spin in \(z\)-direction times 2"
    )

    isospin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Total isospin times 2"
    )

    isospin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Isospin in \(z\)-direction times 2"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "strangeness",
                    "irrep",
                    "embedding",
                    "parity",
                    "spin_x2",
                    "spin_z_x2",
                    "isospin_x2",
                    "isospin_z_x2",
                ],
                name="unique_hadron_hadron4d",
            )
        ]

    def check_consistency(self):
        if self.parity not in [-1, 1]:
            raise ValueError("Parity not in [-1, 1].")
        if abs(self.spin_z_x2) > self.spin_x2:
            raise ValueError("Magnitude of spin_z is greater than spin.")
        if abs(self.isospin_z_x2) > self.isospin_x2:
            raise ValueError("Magnitude of isospin_z is greater than isospin.")


class Hadron(SCSWaveFunction):
    r"""
    Hadronic interpolating operators.
    Momentum projection is performed here.
    The entries should have counterparts at `wavefunction.hadron4d`.
    Reference to Basak operators: https://arxiv.org/abs/hep-lat/0508018.
    """
    description = models.TextField(
        null=True, blank=True, help_text="Description of the interpolating operator",
    )
    strangeness = models.PositiveSmallIntegerField(
        null=False, help_text="Strangeness of hadronic operator",
    )
    irrep = models.TextField(
        null=False,
        blank=False,
        help_text="Irreducible representations of O^D_h (octahedral group)",
    )
    embedding = models.PositiveSmallIntegerField(
        null=False,
        blank=True,
        help_text="k-th embedding of O^D_h irrep., can be blank",
    )

    parity = models.SmallIntegerField(
        null=False, help_text="Parity of hadronic operator"
    )
    spin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Total spin times 2"
    )

    spin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Spin in \(z\)-direction"
    )

    isospin_x2 = models.PositiveSmallIntegerField(
        null=False, help_text="Total isospin times 2"
    )

    isospin_z_x2 = models.SmallIntegerField(
        null=False, help_text="Isospin in \(z\)-direction times 2"
    )

    nx = models.SmallIntegerField(help_text="Momentum in units of 2 pi / L")

    ny = models.SmallIntegerField(help_text="Momentum in units of 2 pi / L")

    nz = models.SmallIntegerField(help_text="Momentum in units of 2 pi / L")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "strangeness",
                    "irrep",
                    "embedding",
                    "parity",
                    "spin_x2",
                    "spin_z_x2",
                    "isospin_x2",
                    "isospin_z_x2",
                    "nx",
                    "ny",
                    "nz",
                ],
                name="unique_hadron_hadron",
            )
        ]

    def check_consistency(self):
        if self.parity not in [-1, 1]:
            raise ValueError("Parity not in [-1, 1].")
        if abs(self.spin_z_x2) > self.spin_x2:
            raise ValueError("Magnitude of spin_z is greater than spin.")
        if abs(self.isospin_z_x2) > self.isospin_x2:
            raise ValueError("Magnitude of isospin_z is greater than isospin.")
