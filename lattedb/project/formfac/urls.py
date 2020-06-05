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
        "disk-ff4d-concat-status",
        DiskConcatenatedFormFactor4DStatusView.as_view(),
        name="Concatenated Form Factor 4D Disk Status",
    ),
    path(
        "tape-ff4d-concat-status",
        TapeConcatenatedFormFactor4DStatusView.as_view(),
        name="Concatenated Form Factor 4D Tape Status",
    ),
    path(
        "disk-ff4d-sliced-averaged-status",
        DiskTSlicedSAveragedFormFactor4DStatusView.as_view(),
        name="Sliced Averaged Form Factor 4D Disk Status",
    ),
    path(
        "tape-ff4d-sliced-averaged-status",
        TapeTSlicedSAveragedFormFactor4DStatusView.as_view(),
        name="Sliced Averaged Form Factor 4D Tape Status",
    ),
    path(
        "disk-ff4d-sliced-status",
        DiskTSlicedFormFactor4DStatusView.as_view(),
        name="Sliced Form Factor 4D Disk Status",
    ),
    path(
        "disk-ff4d-status",
        DiskFormFactor4DStatusView.as_view(),
        name="Form Factor 4D Disk Status",
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
        "disk-spec4d-sliced-averaged-status",
        DiskTSlicedSAveragedSpectrum4DStatusView.as_view(),
        name="Sliced Averaged Spectrum 4D Disk Status",
    ),
    path(
        "tape-spec4d-sliced-averaged-status",
        TapeTSlicedSAveragedSpectrum4DStatusView.as_view(),
        name="Sliced Averaged Spectrum 4D Tape Status",
    ),
    path(
        "disk-spec4d-sliced-status",
        DiskTSlicedSpectrum4DStatusView.as_view(),
        name="Sliced Spectrum 4D Disk Status",
    ),
    path(
        "disk-spec4d-status",
        DiskSpectrum4DStatusView.as_view(),
        name="Spectrum 4D Disk Status",
    ),
]
