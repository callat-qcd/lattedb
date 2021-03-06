from django.db import models

from espressodb.base.models import Base


class Current(Base):
    """
    Base table for application.
    All types of currents are listed here.
    If applicable, consistency is enforced in check_consistency under each table that references `current.current`.
    """


class Local(Current):
    """ Momentum space current
    """

    diracstruct = models.TextField(
        null=False, blank=False, help_text="Dirac structure of the current"
    )

    nx = models.SmallIntegerField(help_text="Current insertion momentum in units of 2 pi / L")

    ny = models.SmallIntegerField(help_text="Current insertion momentum in units of 2 pi / L")

    nz = models.SmallIntegerField(help_text="Current insertion momentum in units of 2 pi / L")

    description = models.TextField(
        null=True, blank=True, help_text="Description of current"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diracstruct", "nx", "ny", "nz"], name="unique_current_local"
            )
        ]

class Local4D(Current):
    """ Spatial current
    """

    diracstruct = models.TextField(
        null=False, blank=False, help_text="Dirac structure of the current"
    )

    description = models.TextField(
        null=True, blank=True, help_text="Description of current"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diracstruct"], name="unique_current_local4d"
            )
        ]
