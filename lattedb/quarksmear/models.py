from django.db import models

from espressodb.base.models import Base


class QuarkSmear(Base):
    r"""
    Base table for application.
    All types of quark smearings (interpolating operator smearing) are listed here.
    If applicable, consistency is enforced in check_consistency under each table that references `quarksmear.quarksmear`.
    """

    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the quark smearing operator",
    )


class Point(QuarkSmear):
    """
    Table for unsmeared operators.
    The table should only have one row with a foreign key.
    """


class GaugeCovariantGaussian(QuarkSmear):
    """
    Gauge invariant Gaussian smearing
    """

    radius = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        help_text="Smearing radius in lattice units",
    )
    step = models.PositiveSmallIntegerField(
        help_text="Number of smearing steps"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["radius", "step"],
                name="unique_qaurksmear_gaugecovariantgaussian",
            )
        ]
