"""Views for the Form Factor project
"""
from abc import ABC

from django.views.generic import TemplateView

from lattedb.utilities.tables import to_table
from lattedb.project.formfac.models import DiskFormFactor4DFile, TapeFormFactor4DFile


class IndexView(TemplateView):
    """Index view of the Form Factor project
    """

    template_name = "formfac-index.html"


class FileStatusView(TemplateView, ABC):
    """Status view for Form Factor files.

    This view is abstract. You should use the Disk and tape specific views.
    """

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
        "exits": "Exists",
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

        print(df.columns)

        count = df["Exists"].value_counts()

        context["status"] = {
            "done": count.get(True),
            "pending": count.get(False),
            "total": count.sum(),
        }
        context["title"] = "Status view for Form Factor files"
        context["subtitle"] = "Considering files on tape"
        context["table"], context["script"] = to_table(df, id_name="File information")

        return context


class DiskStatusView(FileStatusView):
    model = DiskFormFactor4DFile


class TapeStatusView(FileStatusView):
    model = TapeFormFactor4DFile
