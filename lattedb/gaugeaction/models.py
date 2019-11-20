from django.db import models

from espressodb.base.models import Base


class GaugeAction(Base):
    r"""
    Base table for application.
    All types of gauge actions are listed here.
    If applicable, consistency is enforced in check_consistency under each table that references `gaugeaction.gaugeaction`.
    """


class LuescherWeisz(GaugeAction):
    """
    Table for L\"uscher-Weisz action parameters.
    """

    beta = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Strong coupling constant",
    )
    a_fm = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        help_text="Lattice spacing in fermi",
    )
    u0 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Tadpole improvement coefficient",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["beta", "u0"], name="unique_gaugeaction_luescherweisz"
            )
        ]
