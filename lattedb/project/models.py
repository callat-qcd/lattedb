from espressodb.base.models import Base
from django.db import models

class Data(Base):
    """Abstract base table for data
    """

    real = models.FloatField(
        null=False,
        help_text="Float: Real part of data"
    )

    imag = models.FloatField(
        null=False,
        help_text="Float: Imaginary part of data",
    )

    class Meta:
        abstract = True


class Project(Base):
    """Abstract base table for projects
    """

    class Meta:
        abstract = True
