"""Custom django rest tables paginator to render progress bar dynamically
"""
from typing import Optional

from rest_framework_datatables.pagination import DatatablesPageNumberPagination


class Paginator(DatatablesPageNumberPagination):
    """Custom paginator which adds `recordsExist` to json context.
    """

    #: Number of files which exist on tape / disk within filtered query.
    recordsExist: Optional[int] = None

    def paginate_queryset(self, queryset, request, view=None):
        """Paginates queryset and sets `recordsExist`.
        """
        entry = queryset.first()

        pages = super().paginate_queryset(queryset, request, view=view)

        self.recordsExist = (  # pylint:disable=C0103
            queryset.filter(exists=True).count()
            if entry
            and "exists" in set(field.name for field in entry.get_open_fields())
            else None
        )
        return pages

    def get_paginated_response(self, data):
        """Renders respons and adds `recordsExist` to response data.
        """
        response = super().get_paginated_response(data)
        response.data["recordsExist"] = self.recordsExist if self.recordsExist else 0
        return response
