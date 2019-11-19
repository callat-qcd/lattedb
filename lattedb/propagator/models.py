from typing import Dict, Any
from django.db import models

from espressodb.base.models import Base


class Propagator(Base):
    r"""
    Base table for application.
    All types of propagators are listed here.
    Consistency is enforced in check_consistency under each table that references \(\texttt{propagator.propagator}\).
    """


class OneToAll(Propagator):
    """
    General table for a one-to-all propagator.
    Table is independent of sea and valence action.
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to specific \texttt{gaugeconfig} inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to valence lattice \(\texttt{fermionaction}\)."
        " This is the valence action.",
    )
    origin_x = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="x-coordinate origin location of the propagator",
    )
    origin_y = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="y-coordinate origin location of the propagator",
    )
    origin_z = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="z-coordinate origin location of the propagator",
    )
    origin_t = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        help_text="t-coordinate origin location of the propagator",
    )
    sourcesmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to source \(\texttt{quarksmear}\)",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sink \(\texttt{quarksmear}\)",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "fermionaction",
                    "origin_x",
                    "origin_y",
                    "origin_z",
                    "origin_t",
                    "sourcesmear",
                    "sinksmear",
                ],
                name="unique_propagator_onetoall",
            )
        ]


class CoherentSeq(Propagator):
    """
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key referencing specific \(\texttt{gaugeconfig}\) inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key referencing valence lattice \(\texttt{fermionaction}\)",
    )
    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key referencing OneToAll \(\texttt{propagator}\) (spectator 0)",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key referencing OneToAll \(\texttt{propagator}\) (spectator 1)",
    )
    groupsize = models.PositiveSmallIntegerField(
        help_text="Total number of propagators sharing a coherent sink"
    )
    groupindex = models.PositiveSmallIntegerField(
        help_text="Group index indicating which coherent sink group the propagator belongs to"
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key referencing sink interpolating operator \(\texttt{wavefunction}\)",
    )
    sinksep = models.SmallIntegerField(help_text="Source-sink separation time")
    sourcesmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key referencing source \(\texttt{quarksmear}\)",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key referencing sink \(\texttt{quarksmear}\)",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "fermionaction",
                    "propagator0",
                    "propagator1",
                    "groupsize",
                    "groupindex",
                    "sourcesmear",
                    "sinksmear",
                    "sinkwave",
                    "sinksep",
                ],
                name="unique_propagator_coherentseq",
            )
        ]

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["propagator0"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator0 type OneToAll.")
        if data["propagator1"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator1 type OneToAll.")
        if data["propagator0"].id > data["propagator1"].id:
            raise ValueError("Requires propagator0.id <= propagator1.id.")


class FeynmanHellmann(Propagator):
    """
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to specific \(\texttt{gaugeconfig}\) inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to valence lattice \(\texttt{fermionaction}\)",
    )
    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key linking RHS OneToAll \(\texttt{propagator}\)",
    )
    current = models.ForeignKey(
        "current.Current",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key linking momentum space \(\texttt{current}\) insertion",
    )
    sourcesmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to source \(\texttt{quarksmear}\)",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sink \(\texttt{quarksmear}\)",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "fermionaction",
                    "propagator",
                    "current",
                    "sourcesmear",
                    "sinksmear",
                ],
                name="unique_propagator_feynmanhellmann",
            )
        ]

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["propagator"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator type OneToAll.")
