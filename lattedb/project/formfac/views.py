"""Views for the Form Factor project
"""
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Index view of the Form Factor project
    """

    template_name = "formfac-index.html"
