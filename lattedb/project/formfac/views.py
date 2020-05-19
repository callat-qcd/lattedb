# pylint: disable=C0111, R0901
"""Views for the Form Factor project
"""
from abc import ABC

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from lattedb.project.formfac.models import DiskConcatenatedFormFactor4DFile
from lattedb.project.formfac.models import TapeConcatenatedFormFactor4DFile
from lattedb.project.formfac.models import DiskTSlicedSAveragedFormFactor4DFile
from lattedb.project.formfac.models import TapeTSlicedSAveragedFormFactor4DFile
from lattedb.project.formfac.models import TSlicedSAveragedFormFactor4DFile
from lattedb.project.formfac.models import DiskTSlicedFormFactor4DFile
from lattedb.project.formfac.models import DiskFormFactor4DFile

from lattedb.project.formfac.models import DiskCorrelatorH5Dset
from lattedb.project.formfac.models import TapeCorrelatorH5Dset
from lattedb.project.formfac.models import CorrelatorMeta

from lattedb.project.formfac.models import DiskTSlicedSAveragedSpectrum4DFile
from lattedb.project.formfac.models import TapeTSlicedSAveragedSpectrum4DFile
from lattedb.project.formfac.models import DiskTSlicedSpectrum4DFile
from lattedb.project.formfac.models import DiskSpectrum4DFile
from lattedb.project.formfac.models import TSlicedSAveragedSpectrum4DFile
from lattedb.project.formfac.models import TSlicedSpectrum4DFile


class IndexView(TemplateView):
    """Index view of the Form Factor project
    """

    template_name = "formfac-index.html"


class FileStatusView(LoginRequiredMixin, TemplateView, ABC):  # pylint: disable=R0901
    """Status view for Form Factor files.

    This view is abstract. You should use the Disk and tape specific views.
    """

    login_url = reverse_lazy("login")
    title = None
    subtitle = None
    model = None
    template_name = "table.html"
    fieldnames = {
        "file.ensemble": "Ens",
        "file.stream": "Stream",
        "file.configuration_range": "Cfg range",
        "file.source_set": "Src set",
        "file.current": "Curr",
        "file.state": "State",
        "file.parity": "Parity",
        "file.flavor": "Flavor",
        "file.spin": "Spin",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }

    def get_context_data(self, **kwargs):
        """Filters model and returns table
        """
        if not self.model:
            raise ValueError(
                "You need to specify a model for initializing a `FileStatusView`."
            )

        context = super().get_context_data(**kwargs)

        instances = self.model.objects.all()

        context["status"] = {
            "done": instances.filter(exists=True).count(),
            "total": instances.count(),
        }
        context["status"]["pending"] = (
            context["status"]["total"] - context["status"]["done"]
        )
        context["model"] = self.model
        context["columns"] = self.fieldnames
        context["api_url"] = (
            reverse_lazy(f"Project formfac:{self.model.__name__.lower()}-list")
            + "?format=datatables"
        )

        context["title"] = self.title or self.model.verbose_name
        context["subtitle"] = self.subtitle or self.model.get_doc()

        return context


class MetaStatusView(LoginRequiredMixin, TemplateView, ABC):  # pylint: disable=R0901
    """Status view for file meta information.

    This view is abstract. You should use the Disk and tape specific views.
    """

    login_url = reverse_lazy("login")
    title = None
    subtitle = None
    model = None
    template_name = "table.html"
    fieldnames = {
        "ensemble": "Ens",
        "stream": "Stream",
        "configuration_range": "Cfg range",
        "source_set": "Src set",
        "current": "Curr",
        "state": "State",
        "parity": "Parity",
        "flavor": "Flavor",
        "spin": "Spin",
    }

    def get_context_data(self, **kwargs):
        """Filters model and returns table
        """
        if not self.model:
            raise ValueError(
                "You need to specify a model for initializing a `FileStatusView`."
            )

        context = super().get_context_data(**kwargs)

        instances = self.model.objects.all()

        context["status"] = {
            "done": 0,
            "total": instances.count(),
        }
        context["status"]["pending"] = (
            context["status"]["total"] - context["status"]["done"]
        )
        context["model"] = self.model
        context["columns"] = self.fieldnames
        context["api_url"] = (
            reverse_lazy(f"Project formfac:{self.model.__name__.lower()}-list")
            + "?format=datatables"
        )

        context["title"] = self.title or self.model.verbose_name
        context["subtitle"] = self.subtitle or self.model.get_doc()

        return context


# -------------------------------------
# Form Factor
# -------------------------------------


class DiskConcatenatedFormFactor4DStatusView(FileStatusView):
    model = DiskConcatenatedFormFactor4DFile


class TapeConcatenatedFormFactor4DStatusView(FileStatusView):
    model = TapeConcatenatedFormFactor4DFile


class DiskTSlicedSAveragedFormFactor4DStatusView(FileStatusView):
    model = DiskTSlicedSAveragedFormFactor4DFile
    fieldnames = {
        "file.ensemble": "Ens",
        "file.stream": "Stream",
        "file.source_set": "Src set",
        "file.configuration": "Cfg",
        "file.t_separation": "T sep",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }


class TapeTSlicedSAveragedFormFactor4DStatusView(FileStatusView):
    model = TapeTSlicedSAveragedFormFactor4DFile
    fieldnames = {
        "file.ensemble": "Ens",
        "file.stream": "Stream",
        "file.source_set": "Src set",
        "file.configuration": "Cfg",
        "file.t_separation": "T sep",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }


class DiskTSlicedFormFactor4DStatusView(FileStatusView):
    model = DiskTSlicedFormFactor4DFile
    fieldnames = {
        "file.ensemble": "Ens",
        "file.stream": "Stream",
        "file.source_set": "Src set",
        "file.configuration": "Cfg",
        "file.t_separation": "T sep",
        "file.source": "Src",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }


class DiskFormFactor4DStatusView(FileStatusView):
    model = DiskFormFactor4DFile
    fieldnames = {
        "file.ensemble": "Ens",
        "file.stream": "Stream",
        "file.source_set": "Src set",
        "file.configuration": "Cfg",
        "file.t_separation": "T sep",
        "file.source": "Src",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }


class NonExistentSlicedSAveragedFormFactor4DView(MetaStatusView):
    """Presents sliced and avereged ff4d meta entries which are neither on tape nor disk
    """

    title = "Non-existent t-sliced & averaged Form Factor 4D entries"
    subtitle = (
        "This view presents t-sliced & averaged Form Factor 4D entries"
        " which are neither on file, nor on tape."
    )
    model = TSlicedSAveragedFormFactor4DFile
    fieldnames = {
        "ensemble": "Ens",
        "stream": "Stream",
        "source_set": "Src set",
        "configuration": "Cfg",
        "t_separation": "T sep",
    }


# -------------------------------------
# Correlator
# -------------------------------------


class DiskCorrelatorH5DsetStatusView(FileStatusView):
    model = DiskCorrelatorH5Dset
    fieldnames = {
        "meta.correlator": "Corr",
        "meta.ensemble": "Ens",
        "meta.stream": "Stream",
        "meta.configuration": "Cfg",
        "meta.source_set": "Src set",
        "meta.source": "Src",
        "exists": "Exists",
        "machine": "Machine",
        "date_modified": "Date",
    }


class TapeCorrelatorH5DsetStatusView(FileStatusView):
    model = TapeCorrelatorH5Dset
    fieldnames = {
        "meta.correlator": "Corr",
        "meta.ensemble": "Ens",
        "meta.stream": "Stream",
        "meta.configuration": "Cfg",
        "meta.source_set": "Src set",
        "meta.source": "Src",
        "exists": "Exists",
        "machine": "Machine",
        "date_modified": "Date",
    }


class NonExistentCorrelatorH5DsetView(MetaStatusView):
    """Presents sliced and avereged correlator meta entries which are neither on tape
    nor disk
    """

    title = "Non-existent correlator entries"
    subtitle = (
        "This view presents correlator entries"
        " which are neither on file, nor on tape."
    )
    model = CorrelatorMeta
    fieldnames = {
        "correlator": "Corr",
        "ensemble": "Ens",
        "stream": "Stream",
        "configuration": "Cfg",
        "source_set": "Src set",
        "source": "Src",
    }


# -------------------------------------
# Spectrum
# -------------------------------------


class DiskTSlicedSAveragedSpectrum4DStatusView(
    DiskTSlicedSAveragedFormFactor4DStatusView
):
    model = DiskTSlicedSAveragedSpectrum4DFile


class TapeTSlicedSAveragedSpectrum4DStatusView(
    TapeTSlicedSAveragedFormFactor4DStatusView
):
    model = TapeTSlicedSAveragedSpectrum4DFile


class DiskTSlicedSpectrum4DStatusView(DiskTSlicedFormFactor4DStatusView):
    model = DiskTSlicedSpectrum4DFile


class DiskSpectrum4DStatusView(DiskFormFactor4DStatusView):
    model = DiskSpectrum4DFile


class NonExistentSlicedSAveragedSpectrum4DView(MetaStatusView):
    """Presents sliced and avereged ff4d meta entries which are neither on tape nor disk
    """

    title = "Non-existent t-sliced & averaged Spectrum 4D entries"
    subtitle = (
        "This view presents t-sliced & averaged Spectrum 4D entries"
        " which are neither on file, nor on tape."
    )
    model = TSlicedSAveragedSpectrum4DFile
    fieldnames = {
        "ensemble": "Ens",
        "stream": "Stream",
        "source_set": "Src set",
        "configuration": "Cfg",
        "t_separation": "T sep",
    }


class NonExistentSlicedSpectrum4DView(MetaStatusView):
    """Presents sliced and avereged ff4d meta entries which are neither on tape nor disk
    """

    title = "Non-existent t-sliced Spectrum 4D entries"
    subtitle = (
        "This view presents t-sliced Spectrum 4D entries"
        " which are neither on file, nor on tape."
    )
    model = TSlicedSpectrum4DFile
    fieldnames = {
        "ensemble": "Ens",
        "stream": "Stream",
        "source_set": "Src set",
        "configuration": "Cfg",
        "t_separation": "T sep",
        "source": "Src",
    }
