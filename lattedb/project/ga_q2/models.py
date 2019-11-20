"""Models of ga_q2
"""
from typing import Optional, Dict, Any

import os
import datetime
import pytz

from pandas import DataFrame

from django.db import models
from espressodb.base.models import Base
from lattedb.propagator.models import OneToAll


class OneToAllStatus(Base):
    """Status of the one-to-all propagator files
    """

    propagator = models.ForeignKey(
        OneToAll,
        on_delete=models.CASCADE,
        help_text="The one-to-all propagator describing properties of this file.",
    )
    machine = models.CharField(
        max_length=120, help_text="The machine hosting the file."
    )
    file_location = models.TextField(help_text="The path to the file.")
    file_size = models.PositiveIntegerField(
        null=True, help_text="The size of the file in Bytes."
    )
    mtime = models.DateTimeField(
        null=True, help_text="The last time the file was modified."
    )
    exists = models.BooleanField(
        default=False, help_text="File exists at `file_location` on `machine`"
    )
    src_set = models.CharField(
        max_length=40, help_text="The source group the file belongs to. E.g., `0-8`"
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-docstring
        unique_together = ["propagator", "machine", "file_location", "src_set"]

    @staticmethod
    def get_file_info(file_location: str, timezone="Etc/GMT-5") -> Dict[str, Any]:
        """Returns dict with keys ``file_size``, ``mtime``, ``exists`` and ``file_location``

        Arguments:
            file_location: The file path to check
            timezone: The local timezone
        """
        exists = os.path.exists(file_location)

        data = {"exists": exists, "file_location": file_location}

        if exists:
            local = pytz.timezone(timezone)
            utc = pytz.timezone("UTC")

            stats = os.stat(file_location)

            data["file_size"] = int(stats.st_size)
            data["mtime"] = (
                datetime.datetime.fromtimestamp(stats.st_mtime)
                .replace(tzinfo=local)
                .astimezone(utc)
            )
        else:
            data["file_size"] = None
            data["mtime"] = None

        return data

    @classmethod
    def get_summary(
        cls,
        query: Optional[Dict[str, Any]] = None,
        columns=(
            "propagator__gaugeconfig__nf211__short_tag",
            "propagator__gaugeconfig__nf211__stream",
            "propagator__gaugeconfig__nf211__config",
            "propagator__origin_x",
            "propagator__origin_y",
            "propagator__origin_z",
            "src_set",
            "propagator__fermionaction__mobiusdw__quark_mass",
            "exists",
            "file_size",
            "mtime",
            "file_location",
        ),
    ) -> DataFrame:
        """Returns a summary table for the given query.

        Arguments:
            query:
            Dictionary of field lookups. Uses Django's filter.
            columns:
                The columns which will be present in the DataFrame.
                The final column name will be the last string after a ``__``.

        Note:
            See also https://docs.djangoproject.com/en/2.2/topics/db/queries/ for
            lookups.
        """
        qs = cls.objects.filter(**query) if query else cls.objects.all()
        df = qs.to_dataframe(fieldnames=columns, index="id")
        return df.rename(columns={col: col.split("__")[-1] for col in df.columns})
