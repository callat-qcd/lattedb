# pylint: disable=C0103
"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import include

from lattedb.project.formfac.views import DiskConcatenatedFormFactor4DStatusView
from lattedb.project.formfac.views import TapeConcatenatedFormFactor4DStatusView
from lattedb.project.formfac.views import DiskTSlicedSAveragedFormFactor4DStatusView
from lattedb.project.formfac.views import TapeTSlicedSAveragedFormFactor4DStatusView
from lattedb.project.formfac.views import DiskTSlicedFormFactor4DStatusView
from lattedb.project.formfac.views import DiskFormFactor4DStatusView

from lattedb.project.formfac.views import DiskCorrelatorH5DsetStatusView
from lattedb.project.formfac.views import TapeCorrelatorH5DsetStatusView

from lattedb.project.formfac.views import DiskTSlicedSAveragedSpectrum4DStatusView
from lattedb.project.formfac.views import TapeTSlicedSAveragedSpectrum4DStatusView
from lattedb.project.formfac.views import DiskTSlicedSpectrum4DStatusView
from lattedb.project.formfac.views import DiskSpectrum4DStatusView

from lattedb.project.formfac.rest.serializers import ROUTER

app_name = "Project formfac"
urlpatterns = [
    path(r"api/", include(ROUTER.urls)),
    path(
        "disk-concat-status",
        DiskConcatenatedFormFactor4DStatusView.as_view(),
        name="Concatenated Form Factor Disk Status",
    ),
    path(
        "tape-concat-status",
        TapeConcatenatedFormFactor4DStatusView.as_view(),
        name="Concatenated Form Factor Tape Status",
    ),
    path(
        "disk-sliced-averaged-status",
        DiskTSlicedSAveragedFormFactor4DStatusView.as_view(),
        name="Sliced Averaged Form Factor Disk Status",
    ),
    path(
        "tape-sliced-averaged-status",
        TapeTSlicedSAveragedFormFactor4DStatusView.as_view(),
        name="Sliced Averaged Form Factor Tape Status",
    ),
    path(
        "disk-sliced-status",
        DiskTSlicedFormFactor4DStatusView.as_view(),
        name="Sliced Form Factor Disk Status",
    ),
    path(
        "disk-status",
        DiskFormFactor4DStatusView.as_view(),
        name="Form Factor Disk Status",
    ),
    path(
        "disk-corr-status",
        DiskCorrelatorH5DsetStatusView.as_view(),
        name="Correlator Disk Status",
    ),
    path(
        "tape-corr-status",
        TapeCorrelatorH5DsetStatusView.as_view(),
        name="Correlator Tape Status",
    ),
    path(
        "disk-spec-sliced-averaged-status",
        DiskTSlicedSAveragedSpectrum4DStatusView.as_view(),
        name="Sliced Averaged Spectrum Disk Status",
    ),
    path(
        "tape-spec-sliced-averaged-status",
        TapeTSlicedSAveragedSpectrum4DStatusView.as_view(),
        name="Sliced Averaged Spectrum Tape Status",
    ),
    path(
        "disk-spec-sliced-status",
        DiskTSlicedSpectrum4DStatusView.as_view(),
        name="Sliced Spectrum Disk Status",
    ),
    path(
        "disk-spec-status",
        DiskSpectrum4DStatusView.as_view(),
        name="Spectrum Disk Status",
    ),
]
