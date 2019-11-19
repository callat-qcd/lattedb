from typing import Dict, Any
from django.db import models
from django.core.exceptions import ValidationError

from espressodb.base.models import Base


class Correlator(Base):
    r"""
    Base table for application.
    All types of correlators are listed here.
    If applicable, consistency is enforced in check_consistency under each table that references $\texttt{correlator.correlator}$.
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
        help_text=r"Foreign Key to $\texttt{propagator}$",
    )
    wave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to source spin color space $\texttt{wavefunction}$",
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

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["propagator"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator type OneToAll.")
        if data["propagator"].type.fermionaction.type not in ["MobiusDW"]:
            rasise TypeError("Requires propagator action to be MobiusDW.")


class Meson2pt(Correlator):
    """
    All types of meson two point correlators are listed here.
    For specific hadrons and actions, query through foreign key references.
    """
    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to first $\texttt{propagator}$",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to second $\texttt{propagator}$, and must be $\leq \texttt{propagator0}$ (also Foreign Key)",
    )
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to source interpolating operator $\texttt{wavefunction}$",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to sink interpolating operator $\texttt{wavefunction}$",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["propagator0", "propagator1", "sourcewave", "sinkwave"],
                name="unique_correlator_meson2pt",
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
        help_text=r"Foreign Key to first $\texttt{propagator}$",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to second $\texttt{propagator}$, and must be $\leq \texttt{propagator0}$ (also Foreign Key)",
        help_text=r"Foreign Key to second $\texttt{propagator}$, and must be $\leq \texttt{propagator0}$ (also Foreign Key)",
    )
    propagator2 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to third $\texttt{propagator}$, and must be $\leq \texttt{propagator1}$ (also Foreign Key)",
    )
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to source interpolating operator $\texttt{wavefunction}$",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key to sink interpolating operator $\texttt{wavefunction}$",
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

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["propagator0"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator0 type OneToAll.")
        if data["propagator1"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator1 type OneToAll.")
        if data["propagator2"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator2 type OneToAll.")
        if data["propagator0"].id > data["propagator1"].id:
            raise ValueError("Requires propagator0.id <= propagator1.id.")
        if data["propagator1"].id > data["propagator2"].id:
            raise ValueError("Requires propagator1.id <= propagator2.id.")

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
    All types of baryon three point correlators created with a $\texttt{CoherentSeq}$ propagator are listed here.
    For specific hadrons and actions, query through foreign key references.
    """
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to source operator $\texttt{wavefunction}$",
    )
    current = models.ForeignKey(
        "current.Current",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key to current interaction operator $\texttt{wavefunction}$",
    )
    seqpropagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sequential $\texttt{propagator}$ (2 spectator quarks + 1 daughter)",
    )
    propagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to daughter quark $\texttt{propagator}$",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sourcewave", "current", "seqpropagator", "propagator"],
                name="unique_correlator_baryonseq3pt",
            )
        ]

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["propagator"].type not in ["OneToAll"]:
            raise TypeError(r"Requires propagator type OneToAll.")
        if data["seqpropagator"].type not in ["CoherentSeq"]:
            raise TypeError(r"Requires seqpropagator type CoherentSeq.")


class BaryonFH3pt(Correlator):
    r"""
    All types of baryon three point correlators created with a $\texttt{FeynmanHellmann}$ propagator are listed here.
    For specific hadrons and actions, query through foreign key references.
    """
    sourcewave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to source operator $\texttt{wavefunction}$",
    )
    sinkwave = models.ForeignKey(
        "wavefunction.SCSWaveFunction",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to sink operator $\texttt{wavefunction}$",
    )

    fhpropagator = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to Feynman-Hellmann $\texttt{propagator}$",
    )
    propagator0 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to spectator $\texttt{propagator}$",
    )
    propagator1 = models.ForeignKey(
        "propagator.Propagator",
        on_delete=models.CASCADE,
        related_name="+",
        help_text=r"Foreign Key pointing to spectator $\texttt{propagator}$",
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

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["propagator0"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator0 type OneToAll.")
        if data["propagator1"].type not in ["OneToAll"]:
            raise TypeError("Requires propagator1 type OneToAll.")
        if data["fhpropagator"].type not in ["FeynmanHellmann"]:
            raise TypeError("Requires fhpropagator type FeynmanHellmann.")
        if data["propagator0"].id > data["propagator1"].id:
            raise ValueError("Requires propagator0.id <= propagator1.id.")
