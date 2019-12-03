from typing import Dict, Any
from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.core.exceptions import ValidationError

from espressodb.base.models import Base
from espressodb.base.exceptions import ConsistencyError


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

    def check_consistency(self):
        if self.origin_x >= self.gaugeconfig.nx:
            raise ValueError("Origin outside of lattice.")
        if self.origin_y >= self.gaugeconfig.ny:
            raise ValueError("Origin outside of lattice.")
        if self.origin_z >= self.gaugeconfig.nz:
            raise ValueError("Origin outside of lattice.")
        if self.origin_t >= self.gaugeconfig.nt:
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
        help_text=r"Foreign Key pointing to sink `quarksmear` which should be Point unless some bizarre calculation",
    )
    sinksep = models.SmallIntegerField(help_text="Source-sink separation time")

    def check_m2m_consistency(self, propagators, column=None):
        """Checks if all propagators in a coherent source have:
        same prop type (OneToAll)
        same fermion action type in group (can differ in mass)
        same gauge configuration id
        all prop have same source and sink smearing
        """
        first = propagators.first()

        for prop in propagators.all():
            if prop.type not in ["OneToAll"]:
                raise TypeError(f"Spectator {column} is not a OneToAll propagator.")

    def check_all_consistencies(self, props0, props1):
        """Checks if all propagators in a coherent source have:
        prop0 and prop1 have same length
        same prop type (OneToAll)
        same fermion action type (can differ in mass)
        same gauge configuration id
        pairwise prop0.id <= prop1.id
        pairwise same origin
        all prop0 and prop1 have same source and sink smearing
        """
        try:
            self.check_consistency()
            self.check_m2m_consistency(props0, "propagator0")
            self.check_m2m_consistency(props1, "propagator1")

            ### Sanity check
            if props0.count() != props1.count():
                raise ValidationError(
                    f"Set length for propagator0 not equal propagator1."
                )
            ### Global consistency checks
            first = props0.first()
            for prop in props0.all() | props1.all():
                if prop.fermionaction.type != first.fermionaction.type:
                    raise TypeError(f"Spectator fermion action type inconsistent.")
                if prop.gaugeconfig.id != self.gaugeconfig.id:
                    raise ValueError(
                        f"Spectator and daughter have different gauge configs."
                    )
                if prop.sourcesmear.id != first.sourcesmear.id:
                    raise TypeError(f"Spectator source smearing id inconsistent.")
                if prop.sinksmear.id != first.sinksmear.id:
                    raise TypeError(f"Spectator sink smearing id inconsistent.")

            ### Pairwise consistency checks
            origin_id_0 = {
                (prop.origin_x, prop.origin_y, prop.origin_z, prop.origin_t): prop.id
                for prop in props0.all()
            }
            origin_id_1 = {
                (prop.origin_x, prop.origin_y, prop.origin_z, prop.origin_t): prop.id
                for prop in props1.all()
            }
            for origin in origin_id_0:
                if origin in list(origin_id_1.keys()):
                    if origin_id_0[origin] > origin_id_1[origin]:
                        raise ValidationError(
                            "Pairwise prop0.id is not <= prop1.id."
                            " This ensures a unique baryon in each row."
                        )
                else:
                    raise ValidationError(
                        "Spectators are not paired at the same origin."
                    )

            ### Unique constraint
            entries0 = BaryonCoherentSeq.objects.filter(
                gaugeconfig=self.gaugeconfig,
                fermionaction=self.fermionaction,
                sinkwave=self.sinkwave,
                sinksmear=self.sinksmear,
                sinksep=self.sinksep,
            ).annotate(c=Count("propagator0")).filter(c=len(props0))
            for prop in props0:
                entries0 = entries0.filter(propagator0=prop)

            entries1 = BaryonCoherentSeq.objects.filter(
                gaugeconfig=self.gaugeconfig,
                fermionaction=self.fermionaction,
                sinkwave=self.sinkwave,
                sinksmear=self.sinksmear,
                sinksep=self.sinksep,
            ).annotate(c=Count("propagator1")).filter(c=len(props1))
            for prop in props1:
                entries1 = entries1.filter(propagator0=prop)

            if entries0.exists() and entries1.exists():
                raise ValidationError(
                    "Unique Constraint Violation. Entry already exists in BaryonCoherentSeq."
                )

        except Exception as error:
            raise ConsistencyError(
                error, self, data={"propagators0": props0, "propagators1": props1}
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
                    "sinksmear",
                ],
                name="unique_propagator_feynmanhellmann",
            )
        ]

    def check_consistency(self):
        if self.propagator.type not in ["OneToAll"]:
            raise TypeError("Requires propagator type OneToAll.")
        if self.propagator.gaugeconfig.id != self.gaugeconfig.id:
            raise TypeError("Parent and daughter are on different gauge configs.")
        if self.propagator.fermionaction.type != self.fermionaction.type:
            raise TypeError(
                """
                Parent and daughter use different types of fermion actions.
                Remove constraint in propagator.models.FeynmanHellmann
                and unittest in propagator.tests if mixed action is needed.
                """
            )
        if self.propagator.sinksmear.type != "Point":
            raise TypeError("Parent propagator is not a Point sink.")
