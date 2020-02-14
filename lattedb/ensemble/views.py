"""Views for the ensemble module
"""
from typing import Dict

from decimal import Decimal

from pandas import DataFrame

from django.views.generic.base import TemplateView

# from lattedb.ensemble.models import Ensemble
from lattedb.gaugeconfig.models import Nf211
from lattedb.gaugeaction.models import LuescherWeisz
from lattedb.fermionaction.models import Hisq


def print_class_html(cls) -> str:
    """Wraps class label with code block
    """
    return f"<code>{cls.get_label()}</code>"


#
# class EnsembleView(TemplateView):
#     """Views gaugeconfigs for given ensemble
#
#     ToDo:
#         Actually use ensembel and not the tag -> this needs defined ensembles
#     """
#
#     template_name = "table.html"
#
#     hbarc = 197.3269804
#
#     gaugeconfig = Nf211
#     gaugeaction = LuescherWeisz
#     fermionaction = Hisq
#
#     def get_context_data(self, **kwargs):
#         """Prepares the table data
#         """
#         context = super().get_context_data(**kwargs)
#         context["title"] = f"Ensemble view of {print_class_html(self.gaugeconfig)}"
#         context["subtitle"] = (
#             f"Using {print_class_html(self.gaugeaction)}"
#             f" and {print_class_html(self.fermionaction)}"
#         )
#         context["table"] = self.prettify(self.dataframe).to_html(
#             classes="table table-striped table-bordered"
#         )
#
#         return context
#
#     @property
#     def column_map(self) -> Dict[str, str]:
#         """Returns map for actual gaugeconfig columns to how the will be named in
#         the data frame
#         """
#         fermionaction_type = self.fermionaction.__name__.lower()
#         gaugeaction_type = self.gaugeaction.__name__.lower()
#         return {
#             "tag": "tag",
#             "nx": r"\(n_l\)",
#             "nt": r"\(n_t\)",
#             f"light__{fermionaction_type}__quark_mass": r"\(m_l\)",
#             f"strange__{fermionaction_type}__quark_mass": r"\(m_s\)",
#             f"charm__{fermionaction_type}__quark_mass": r"\(m_c\)",
#             f"charm__{fermionaction_type}__naik": "charm naik",
#             f"gaugeaction__{gaugeaction_type}__beta": r"\(\beta\)",
#             f"gaugeaction__{gaugeaction_type}__a_fm": r"\(a\) [fm]",
#             f"gaugeaction__{gaugeaction_type}__u0": r"\(u_0\)",
#             f"mpi": r"\(m_\pi\) [MeV]",
#         }
#
#     @property
#     def dataframe(self) -> DataFrame:
#         """Returns the dataframe of distince gaugeconfig ensembles
#         """
#         df = (
#             Nf211.objects.values_list("tag")
#             .distinct()
#             .to_dataframe(fieldnames=list(self.column_map.keys()))
#             .rename(columns=self.column_map)
#         )
#         df[r"\(L\) [fm]"] = df[r"\(n_l\)"] * df[r"\(a\) [fm]"]
#         df[r"\(m_\pi L\)"] = (
#             (df[r"\(m_\pi\) [MeV]"] * df[r"\(L\) [fm]"]).astype(float) / self.hbarc
#         ).round(2)
#         return df
#
#     @staticmethod
#     def prettify(dataframe: DataFrame) -> DataFrame:
#         """Removes trailing zeros of decimals
#         """
#         return dataframe.applymap(
#             lambda x: str(x).rstrip("0").rstrip(".") if isinstance(x, Decimal) else x
#         )
