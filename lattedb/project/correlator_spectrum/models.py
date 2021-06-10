"""Models of correlator_spectrum
"""
from django.db import models
from espressodb.base.models import Base

from django_gvar.fields import GVarField
from django.contrib.auth.models import User

# Feel free to adjust the files below
# This is just random stuff...


class Data(Base):
    """Something which lets users uniquely identify the data (and query)."""

    name = models.CharField(max_length=32, help_text="Some name to identify the data")

    def download(self, local_path):
        ...  # some logic to download data to a local path


class FitFunction(Base):
    """Specifies import statement to obtain fit function.

    I.e.,
    ```
    from {module} import {name}
    ```
    """

    name = models.CharField(max_length=100, help_text="Name of the function.")
    module = models.CharField(
        max_length=100, help_text="Module the function is contained in."
    )
    repository = models.URLField(
        null=True, help_text="Git repository to get function from."
    )
    version = models.CharField(
        max_length=100, null=True, help_text="Commit/version of repo."
    )


class Fit(Base):
    """Specification of fit details."""

    data = models.ForeignKey(
        Data,
        on_delete=models.CASCADE,
        help_text="Link to input data information.",
        related_name="fits",
    )
    data = models.ForeignKey(
        FitFunction,
        on_delete=models.CASCADE,
        help_text="Link to fit function used to run this fit.",
        related_name="fits",
    )
    meta = models.JSONField(help_text="Non fit parameter which determine the fit.")
    prior = GVarField(help_text="Prior distributions used in fit")
    posterior = GVarField(help_text="Posterior distributions returned by fit")
    chi2_dof = models.FloatField(help_text="Chi**2 per degree of freedom of fit.")
    logGBF = models.FloatField(help_text="Log Gaussian Bayes factor of fit.")
    statistics = models.JSONField(help_text="Summary statistics for fit.")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who produced the fit.",
        related_name="fits",
    )


class FitSummary(Base):
    """Something which will be used for model averages or so.

    (only average over files with certain rating).
    """

    observable = models.CharField(max_length=100)
    fit = models.ForeignKey(
        Fit,
        on_delete=models.CASCADE,
        help_text="Link to input data information.",
        related_name="fits",
    )
    rating = models.IntegerField()
