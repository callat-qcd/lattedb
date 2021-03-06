from typing import Dict, Any
from django.db import models
from django.core.exceptions import ValidationError

from espressodb.base.models import Base


class Correlator(Base):
    r"""
    Base table for application.
    All types of correlators are listed here.
    If applicable, consistency is enforced in check_consistency under each table that references `correlator.correlator`.
    """


# Create your models here.
class DWFTuning(Correlator):
    """
    Two point correlation functions used to calculate residual mass for domain-wall action.
    """

    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to `propagator`",
    )
    wave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to source spin color space `wavefunction`",
    )
    sink5 = models.BooleanField(null=False, help_text="Is the sink on the domain wall?")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator", "wave", "sink5"],
                name="unique_correlator_dwftuning",
            )
        ]

    def clean(self):
        """Sets tag of the correlator based on sink5.
        """
        if self.tag is None:
            self.tag = "pseudo_pseudo" if self.sink5 else "midpoint_pseudo"

    def check_consistency(self):
        if self.propagator.type not in ["OneToAll"]:
            raise TypeError("Requires propagator type OneToAll.")
        if self.propagator.fermionaction.type not in ["MobiusDW"]:
            raise TypeError("Requires propagator action to be MobiusDW.")


class Meson2pt(Correlator):
    """
    All types of meson two point correlators are listed here.
    For specific hadrons and actions, query through foreign key references.
    """

    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to first `propagator`",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to second `propagator`, and must be \(\leq\) `propagator0` (also Foreign Key)",
    )
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to source interpolating operator `wavefunction`",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to sink interpolating operator `wavefunction`",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator0", "propagator1", "sourcewave", "sinkwave"],
                name="unique_correlator_meson2pt",
            )
        ]

    def check_consistency(self):
        for idx in [0, 1]:
            if getattr(self, f"propagator{idx}").type not in ["OneToAll"]:
                raise TypeError(f"Requires propagator{idx} type OneToAll.")
        if self.propagator0.id > self.propagator1.id:
            raise ValueError("Requires propagator0.id <= propagator1.id.")
        if self.propagator0.gaugeconfig.id != self.propagator1.gaugeconfig.id:
            raise ValidationError(
                "Requires prop0 and prop1 be on same gauge configuration (id constraint)."
            )
        if self.propagator0.sourcesmear.id != self.propagator1.sourcesmear.id:
            raise ValidationError(
                "All propagators required to have same source smearing."
            )
        if self.propagator0.sinksmear.id != self.propagator1.sinksmear.id:
            raise ValidationError(
                "All propagators required to have same sink smearing."
            )

    def clean(self):
        """Sets tag of the correlator based on propagators, the gaugeconfig and source.

        Operators are sorted by their `mval` key.
        """
        p0 = self.propagator0
        p1 = self.propagator1
        if p1 < p0:  # sorted by mval
            self.propagator0 = p1
            self.propagator1 = p0

        if self.tag is None:
            gc0 = self.propagator0.gaugeconfig.specialization  # pylint: disable=E1101
            p0 = self.propagator0.specialization  # pylint: disable=E1101
            gc1 = self.propagator1.gaugeconfig.specialization  # pylint: disable=E1101
            p1 = self.propagator1.specialization  # pylint: disable=E1101

            if gc0 != gc1:
                raise ValidationError(
                    "What are you smoking?"
                    " Propagators not on the same gaugeconfig?!"
                    f"\n{gc0} != {gc1}"
                )

            strangeness = self.source.strangeness  # pylint: disable=E1101
            if abs(strangeness) == 0:  # pylint: disable=E1101
                dtype = "pion"
            elif abs(strangeness) == 1:  # pylint: disable=E1101
                dtype = "kaon"
            elif abs(strangeness) == 2:  # pylint: disable=E1101
                dtype = "etas"
            else:
                raise ValidationError(
                    f"Received strangeness {strangeness} meson."
                    " Don't know how to deal with that..."
                )

            if p1 == p0:
                self.tag = f"{p0.tag}_on_{gc0.tag}_{dtype}"
            else:
                self.tag = f"{p1.tag}{p0.tag}_on_{gc0.tag}_{dtype}"


class Baryon2pt(Correlator):
    """
    All types of baryon two point correlators are listed here.
    For specific hadrons and actions, query through foreign key references.
    """

    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to first `propagator`",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to second `propagator`, and must be \(\leq\) `propagator0` (also Foreign Key)",
    )
    propagator2 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to third `propagator`, and must be \(\leq\) `propagator1` (also Foreign Key)",
    )
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to source interpolating operator `wavefunction`",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to sink interpolating operator `wavefunction`",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "propagator0",
                    "propagator1",
                    "propagator2",
                    "sourcewave",
                    "sinkwave",
                ],
                name="unique_correlator_baryon2pt",
            )
        ]

    def check_consistency(self):
        for idx in [0, 1, 2]:
            if getattr(self, f"propagator{idx}").type not in ["OneToAll"]:
                raise TypeError(f"Requires propagator{idx} type OneToAll.")
        if self.propagator0.id <= self.propagator1.id <= self.propagator2.id:
            pass
        else:
            raise ValueError(
                "Requires propagator0.id <= propagator1.id <= propagator2.id."
            )
        if (
            self.propagator0.gaugeconfig.id
            == self.propagator1.gaugeconfig.id
            == self.propagator2.gaugeconfig.id
        ):
            pass
        else:
            raise ValidationError(
                "Requires prop0, prop1, and prop2 be on same gauge configuration (id constraint)."
            )
        if (
            self.propagator0.sourcesmear.id
            == self.propagator1.sourcesmear.id
            == self.propagator2.sourcesmear.id
        ):
            pass
        else:
            raise ValidationError(
                "All propagators required to have same source smearing."
            )
        if (
            self.propagator0.sinksmear.id
            == self.propagator1.sinksmear.id
            == self.propagator2.sinksmear.id
        ):
            pass
        else:
            raise ValidationError(
                "All propagators required to have same sink smearing."
            )

    def origin(self):
        return "(%d, %d, %d, %d)" % (
            self.propagator0.origin_x,
            self.propagator0.origin_y,
            self.propagator0.origin_z,
            self.propagator0.origin_t,
        )

    origin.short_description = "origin (x, y, z, t)"

    @classmethod
    def get_from_ensemble(
        cls,
        ensemble: "Ensemble",
        propagator: str = "propagator0",
        propagator_type: str = "OneToAll",
    ) -> "QuerySet(Baryon2pt)":
        """Returns all correlators which are associated with the ensemble.

        The association is given through the propagator relation.

        **Arguments**
            ensemble: Ensemble
                The ensemble of gaugeconfigs

            propagator: str = "propagator0"
                The propagator of the correlator associated with the gagugeconfig.
                For this correlator, can be one out of
                `[propagator0, propagator1, propagator2]`, but all should be on the same
                gaugeconfig anyway.

            propagator_type: str = "OneToAll"
                The type of the propagator e.g. "OneToAll".
        """
        table_filter = {
            f"{propagator}"
            f"__{propagator_type.lower()}"
            f"__gaugeconfig__in": ensemble.configurations.all()
        }
        return cls.objects.filter(**table_filter)

    @property
    def n_config(self) -> int:
        """The number of the gaugeconfig.
        """
        return self.propagator0.gaugeconfig.config

    @property
    def short_tag(self) -> str:
        """The short tag of the gaugeconfig.
        """
        return self.propagator0.gaugeconfig.short_tag

    @property
    def stream(self) -> str:
        """The stream of the gaugeconfig.
        """
        return self.propagator0.gaugeconfig.stream


class BaryonSeq3pt(Correlator):
    r"""
    All types of baryon three point correlators created with a `BaryonCoherentSeq` propagator are listed here.
    For specific hadrons and actions, query through foreign key references.
    """
    current = models.ForeignKey(
        "current.Current",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key to current interaction operator `wavefunction`",
    )
    seqpropagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sequential `propagator` (2 spectator quarks + 1 daughter)",
    )
    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to daughter quark `propagator`",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["current", "seqpropagator", "propagator"],
                name="unique_correlator_baryonseq3pt",
            )
        ]

    def check_consistency(self):
        if self.propagator.type not in ["OneToAll"]:
            raise TypeError(r"Requires propagator type OneToAll.")
        if self.seqpropagator.type not in ["BaryonCoherentSeq"]:
            raise TypeError(r"Requires seqpropagator type BaryonCoherentSeq.")
        if self.propagator.sinksmear.type not in ["Point"]:
            raise TypeError(
                f"Propagator sink smear constrained to be Point. Propagator is {self.propagator.sinksmear}. Remove this constraint if you want to do something edgy. Get it? I wrote this after some drinks."
            )
        # check source smearing
        if (
            self.seqpropagator.propagator0.values("onetoall__sourcesmear")
            .filter(id=self.propagator.sourcesmear.id)
            .exists()
        ):
            pass
        else:
            raise TypeError(
                f"Seqprop and Prop constrained to have same source smearing."
            )
        # check gauge config id
        if (
            self.seqpropagator.propagator0.values("onetoall__gaugeconfig_id").first()[
                "onetoall__gaugeconfig_id"
            ]
            != self.propagator.gaugeconfig.id
        ):
            raise ValidationError(
                f"Seqprop and prop constrained to use same gauge configuration (id constraint)."
            )
        # Check same origin between propagator and seqpropagator.
        # seqprop already has prop0 & prop1 origin checks.
        # So checking only prop0 in seqprop is sufficient.
        origin_list = self.seqpropagator.propagator0.values_list(
            *[f"onetoall__origin_{oi}" for oi in ["x", "y", "z", "t"]]
        )
        prop_origin = tuple(
            getattr(self.propagator, f"origin_{oi}") for oi in ["x", "y", "z", "t"]
        )
        if prop_origin in origin_list:
            pass
        else:
            raise ValidationError("Parent does not have same origin as spectators.")


class BaryonFH3pt(Correlator):
    r"""
    All types of baryon three point correlators created with a `FeynmanHellmann` propagator are listed here.
    For specific hadrons and actions, query through foreign key references.
    """
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to source operator `wavefunction`",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sink operator `wavefunction`",
    )

    fhpropagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to Feynman-Hellmann `propagator`",
    )
    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to spectator `propagator`",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to spectator `propagator` where propagator0.id <= propagator1.id is a constraint",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "sourcewave",
                    "fhpropagator",
                    "propagator0",
                    "propagator1",
                    "sinkwave",
                ],
                name="unique_correlator_baryonfh3pt",
            )
        ]

    def check_consistency(self):
        if self.propagator0.type not in ["OneToAll"]:
            raise TypeError("Requires propagator0 type OneToAll.")
        if self.propagator1.type not in ["OneToAll"]:
            raise TypeError("Requires propagator1 type OneToAll.")
        if self.fhpropagator.type not in ["FeynmanHellmann"]:
            raise TypeError("Requires fhpropagator type FeynmanHellmann.")
        if self.propagator0.id > self.propagator1.id:
            raise ValueError("Requires propagator0.id <= propagator1.id.")
        if (
            self.propagator0.sourcesmear.id
            == self.propagator1.sourcesmear.id
            == self.fhpropagator.propagator.sourcesmear.id
        ):
            pass
        else:
            raise ValidationError("All propagators need to have same source smearing.")
        if (
            self.propagator0.sinksmear.id
            == self.propagator1.sinksmear.id
            == self.fhpropagator.propagator.sinksmear.id
        ):
            pass
        else:
            raise ValidationError("All propagators need to have same sink smearing.")
        if (
            self.propagator0.gaugeconfig.id
            == self.propagator1.gaugeconfig.id
            == self.fhpropagator.gaugeconfig.id
        ):
            pass
        else:
            raise ValidationError(
                "Prop0, prop1, and fhprop constrained to be on same gauge configuration (id constraint)."
            )
