from django.db import models

from espressodb.base.models import Base


class LinkSmear(Base):
    """ Base table for application"
    """


class Unsmeared(LinkSmear):
    """
    Empty table for Foreign Key references to unsmeared gauge links.
    """


class WilsonFlow(LinkSmear):
    """
    Wilson flow smearing for gauge links.
    """

    flowtime = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        help_text="Flow time in lattice units",
    )
    flowstep = models.PositiveSmallIntegerField(
        help_text="Number of diffusion steps"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["flowtime", "flowstep"], name="unique_linksmear_wilsonflow"
            )
        ]
