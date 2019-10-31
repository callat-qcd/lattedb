from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from lattedb.project.models import Project


class Fhcompare(Project):
    """ Base table for application
    """

    mn = models.FloatField(null=False, help_text="Float: nucleon mass")

    ga = models.FloatField(null=False, help_text="Float: axial charge")

    gv = models.FloatField(null=False, help_text="Float: vector charge")

    rating = models.SmallIntegerField(
        null=False,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Int: Limit from 1 to 5, default = 1. Rate your own fits.",
    )

    result = models.TextField(
        null=False, blank=False, help_text="Text: {'your_results': 'all dumped here'}"
    )
