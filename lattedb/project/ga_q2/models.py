"""Models of ga_q2
"""
from typing import Dict, Any

import os
import datetime
import pytz

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
    short_tag = models.CharField(
        max_length=20, help_text="Ensemble short quantifier like `a09m130`."
    )
    src_set = models.CharField(
        max_length=40, help_text="The source group the file belongs to. E.g., `0-8`"
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-docstring
        unique_together = ["propagator", "machine", "file_location", "src_set"]

    def check_consistency(self, data):
        """Checks if the ensemble of the propagator is quantified properly
        """
        assert data["propagator"].gaugeconfig.short_tag == data["short_tag"]

    @staticmethod
    def get_file_info(file_path: str, timezone="Etc/GMT-5") -> Dict[str, Any]:
        """Returns dict with keys ``file_size``, ``mtime``, ``exists`` and ``file_path``

        Arguments:
            file_path: The file path to check
            timezone: The local timezone
        """
        exists = os.path.exists(file_path)

        data = {"exists": exists, "file_path": file_path}

        if file_path:
            local = pytz.timezone(timezone)
            utc = pytz.timezone("UTC")

            stats = os.stat(file_path)

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
