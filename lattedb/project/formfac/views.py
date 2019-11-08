"""Views for the Form Factor project
"""
from abc import ABC

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from lattedb.utilities.tables import to_table
from lattedb.project.formfac.models import DiskConcatenatedFormFactor4DFile
from lattedb.project.formfac.models import TapeConcatenatedFormFactor4DFile
from lattedb.project.formfac.models import TapeTSlicedSAveragedFormFactor4DFile
from lattedb.project.formfac.models import DiskTSlicedSAveragedFormFactor4DFile
from lattedb.project.formfac.models import DiskFormFactor4DFile
from lattedb.project.formfac.models import DiskTSlicedFormFactor4DFile


class IndexView(TemplateView):
    """Index view of the Form Factor project
    """

    template_name = "formfac-index.html"


class FileStatusView(LoginRequiredMixin, TemplateView, ABC):  # pylint: disable=R0901
    """Status view for Form Factor files.

    This view is abstract. You should use the Disk and tape specific views.
    """

    login_url = "/login/"

    model = None
    template_name = "table.html"
    fieldnames = {
        # "file__name": "file",
        "file__ensemble": "Ens",
        "file__stream": "Stream",
        "file__configuration_range": "Cfg range",
        "file__source_set": "Src set",
        "file__current": "Curr",
        "file__state": "State",
        "file__parity": "Parity",
        "file__flavor": "Flavor",
        "file__spin": "Spin",
        # "path": "path",
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
        df = self.model.objects.to_dataframe(
            fieldnames=list(self.fieldnames.keys())
        ).rename(columns=self.fieldnames)

        count = df["Exists"].value_counts()

        context["status"] = {
            "done": count.get(True, 0),
            "pending": count.get(False, 0),
            "total": count.sum(),
        }
        context["title"] = "Status view for Form Factor files"
        context["subtitle"] = "Considering files on tape"
        context["table"], context["script"] = to_table(df, id_name="file-information")
        context["model"] = self.model

        return context


class DiskConcatenatedFormFactor4DStatusView(FileStatusView):
    model = DiskConcatenatedFormFactor4DFile


class TapeConcatenatedFormFactor4DStatusView(FileStatusView):
    model = TapeConcatenatedFormFactor4DFile


class DiskTSlicedSAveragedFormFactor4DStatusView(FileStatusView):
    model = DiskTSlicedSAveragedFormFactor4DFile
    fieldnames = {
        # "file__name": "file",
        "file__ensemble": "Ens",
        "file__stream": "Stream",
        "file__source_set": "Src set",
        "file__configuration": "Cfg",
        "file__t_separation": "T sep",
        # "path": "path",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }


class TapeTSlicedSAveragedFormFactor4DStatusView(FileStatusView):
    model = TapeTSlicedSAveragedFormFactor4DFile
    fieldnames = {
        # "file__name": "file",
        "file__ensemble": "Ens",
        "file__stream": "Stream",
        "file__source_set": "Src set",
        "file__configuration": "Cfg",
        "file__t_separation": "T sep",
        # "path": "path",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }


class DiskTSlicedFormFactor4DStatusView(FileStatusView):
    model = DiskTSlicedFormFactor4DFile
    fieldnames = {
        # "file__name": "file",
        "file__ensemble": "Ens",
        "file__stream": "Stream",
        "file__source_set": "Src set",
        "file__configuration": "Cfg",
        "file__t_separation": "T sep",
        "file__source": "Src",
        # "path": "path",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }


class DiskFormFactor4DStatusView(FileStatusView):
    model = DiskFormFactor4DFile
    fieldnames = {
        # "file__name": "file",
        "file__ensemble": "Ens",
        "file__stream": "Stream",
        "file__source_set": "Src set",
        "file__configuration": "Cfg",
        "file__t_separation": "T sep",
        "file__source": "Src",
        # "path": "path",
        "exists": "Exists",
        "machine": "Machine",
        "size": "Size",
        "date_modified": "Date",
    }
