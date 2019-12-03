from django.db import models

from espressodb.base.models import Base

from lattedb.gaugeaction.models import GaugeAction
from lattedb.fermionaction.models import FermionAction


class GaugeConfig(Base):
    r"""
    Base table for application.
    All types of gauge configurations are listed here.
    If applicable, consistency is enforced in check_consistency under each table that references `gaugeconfig.gaugeconfig`.
    """

    def same_ensemble(self, config: "GaugeConfig") -> bool:
        """Checks if all meta information for a given config are the same.
        """
        equal = False
        if self.type == config.type:
            equal = all(
                [
                    getattr(self, column.name) == getattr(config, column.name)
                    for column in self.specialization.get_open_fields()
                    if column.name != "config"
                ]
            )

        return equal


class Nf211(GaugeConfig):
    r"""
    All types of 2+1+1 flavor gauge configurations are listed here.
    For specific valence and sea actions, query through gauge action and quark references.
    In particular, each configuration has its own entry.
    Ensembles can be found in `ensemble.ensemble` which references `gaugeconfig`.
    """

    short_tag = models.TextField(
        null=True, blank=True, help_text="Short name for gaugeconfig (e.g. 'a15m310')"
    )
    stream = models.TextField(
        null=False, blank=False, help_text="Stream tag for Monte Carlo (e.g. 'a')"
    )
    config = models.PositiveSmallIntegerField(
        help_text="Configuration number (usually MC trajectory number)"
    )
    gaugeaction = models.ForeignKey(
        GaugeAction,
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to lattice `gaugeaction`",
    )
    nx = models.PositiveSmallIntegerField(
        null=False, help_text="Spatial length in lattice units"
    )
    ny = models.PositiveSmallIntegerField(
        null=False, help_text="Spatial length in lattice units"
    )
    nz = models.PositiveSmallIntegerField(
        null=False, help_text="Spatial length in lattice units"
    )
    nt = models.PositiveSmallIntegerField(
        null=False, help_text="Temporal length in lattice units"
    )
    light = models.ForeignKey(
        FermionAction,
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to lattice `fermionaction`",
    )
    strange = models.ForeignKey(
        FermionAction,
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to lattice `fermionaction`",
    )
    charm = models.ForeignKey(
        FermionAction,
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to lattice `fermionaction`",
    )
    mpi = models.PositiveSmallIntegerField(null=True, help_text="Pion mass in MeV")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "stream",
                    "config",
                    "gaugeaction",
                    "nx",
                    "ny",
                    "nz",
                    "nt",
                    "light",
                    "strange",
                    "charm",
                ],
                name="unique_gaugeconfig_nf211",
            )
        ]

    @property
    def long_tag(self) -> str:
        """Returns descriptive long tag representing configuration
        """
        return (
            f"l{self.nx}{self.nt}"  # pylint: disable=E1101
            f"f211"
            f"b{int(self.gaugeaction.beta * 100)}"
            f"m{int(self.light.quark_mass*1000):03d}"
            f"m{int(self.strange.quark_mass*1000):03d}"
            f"m{int(self.charm.quark_mass*1000):03d}"
        )

    def check_consistency(self):
        if self.light.quark_tag not in ["light"]:
            raise TypeError("Requires light to be quark_tag = light in FermionAction.")
        if self.strange.quark_tag not in ["strange"]:
            raise TypeError(
                "Requires strange to be quark_tag = strange in FermionAction."
            )
        if self.charm.quark_tag not in ["charm"]:
            raise TypeError("Requires charm to be quark_tag = charm in FermionAction.")
