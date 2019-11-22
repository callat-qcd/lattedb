from typing import Dict, Any
from django.db import models
from django.core.exceptions import ValidationError

from espressodb.base.models import Base


class Propagator(Base):
    r"""
    Base table for application.
    All types of propagators are listed here.
    Consistency is enforced in check_consistency under each table that references `propagator.propagator`.
    """


class OneToAll(Propagator):
    """
    All one-to-all propagators are listed here.
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to specific \texttt{gaugeconfig} inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to valence lattice `fermionaction`."
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
        help_text=r"Foreign Key pointing to source `quarksmear`",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sink `quarksmear`",
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

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["origin_x"] >= data["gaugeconfig"].nx:
            raise ValueError("Origin outside of lattice.")
        if data["origin_y"] >= data["gaugeconfig"].ny:
            raise ValueError("Origin outside of lattice.")
        if data["origin_z"] >= data["gaugeconfig"].nz:
            raise ValueError("Origin outside of lattice.")
        if data["origin_t"] >= data["gaugeconfig"].nt:
            raise ValueError("Origin outside of lattice.")


class BaryonCoherentSeq(Propagator):
    """
    All coherence sequential propagators are listed here.
    This is for baryons because there are 2 spectator quarks.
    The hadronic operator smearing is already defined in OneToAll propagator.
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key referencing specific `gaugeconfig` inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key referencing valence lattice `fermionaction`",
    )
    propagator0 = models.ManyToManyField(
        to=Propagator,
        related_name="baryoncoherentseq_set0",
        help_text=r"A set of Foreign Keys referencing OneToAll `propagator` (spectator 0) in same source group",
    )
    propagator1 = models.ManyToManyField(
        to=Propagator,
        related_name="baryoncoherentseq_set1",
        help_text=r"A set of Foreign Keys referencing OneToAll `propagator` (spectator 1) in same source group",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key referencing sink interpolating operator `wavefunction`",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sink `quarksmear`",
    )
    sinksep = models.SmallIntegerField(help_text="Source-sink separation time")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "gaugeconfig",
                    "fermionaction",
                    "sinkwave",
                    "sinksmear",
                    "sinksep",
                ],
                name="unique_propagator_baryoncoherentseq",
            )
        ]

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        """Checks if all propagators in a coherent source have:
        prop0 and prop1 have same length
        same prop type (OneToAll)
        same fermion action type (can differ in mass)
        same gauge configuration id
        pairwise prop0.id <= prop1.id
        pairwise same origin
        all prop0 and prop1 have same source and sink smearing
        """
        """Sanity check"""
        if data["propagator0"].count() != data["propagator1"].count():
            raise ValidationError(f"Set length for propagator0 not equal propagator1.")
        """Global consistency checks"""
        first = data["propagator0"].first()
        for idx in [0, 1]:
            for prop in data[f"propagator{idx}"].all():
                if prop.type not in ["OneToAll"]:
                    raise TypeError(f"Spectator {idx} is not a OneToAll propagator.")
                if prop.fermionaction.type != first.fermionaction.type:
                    raise TypeError(
                        f"Spectator {idx} fermion action type inconsistent."
                    )
                print("in check:", prop.gaugeconfig.id, data['gaugeconfig'].id)
                if prop.gaugeconfig.id != data['gaugeconfig'].id:
                    raise ValueError(
                        f"Spectator {idx} and daughter have different gauge configs."
                    )
                if prop.sourcesmear.id != first.sourcesmear.id:
                    raise TypeError(f"Spectator {idx} source smearing id inconsistent.")
                if prop.sinksmear.id != first.sinksmear.id:
                    raise TypeError(f"Spectator {idx} sink smearing id inconsistent.")
        """Pairwise consistency checks"""
        origin_id_0 = {
            (prop.origin_x, prop.origin_y, prop.origin_z, prop.origin_t): prop.id
            for prop in data["propagator0"].all()
        }
        origin_id_1 = {
            (prop.origin_x, prop.origin_y, prop.origin_z, prop.origin_t): prop.id
            for prop in data["propagator1"].all()
        }
        for origin in origin_id_0:
            if origin in list(origin_id_1.keys()):
                if origin_id_0[origin] > origin_id_1[origin]:
                    raise ValidationError(
                        "Pairwise prop0.id is not <= prop1.id. This ensures a unique baryon in each row."
                    )
            else:
                raise ValidationError(
                    "Spectators are not paired at the same origin."
                )

class FeynmanHellmann(Propagator):
    """
    All Feynman-Hellmann type propagators, where the inversion is done at the current insertion, are listed here.
    """

    gaugeconfig = models.ForeignKey(
        "gaugeconfig.GaugeConfig",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to specific `gaugeconfig` inverted on",
    )
    fermionaction = models.ForeignKey(
        "fermionaction.FermionAction",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to valence lattice `fermionaction`",
    )
    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key linking RHS OneToAll `propagator`",
    )
    current = models.ForeignKey(
        "current.Current",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key linking momentum space `current` insertion",
    )
    sourcesmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to source `quarksmear`",
    )
    sinksmear = models.ForeignKey(
        "quarksmear.QuarkSmear",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sink `quarksmear`",
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
