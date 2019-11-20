from typing import Dict
from typing import Any
from typing import Optional

from django.db import models
from django.core.exceptions import ValidationError

from espressodb.base.models import Base

from lattedb.gaugeconfig.models import GaugeConfig


class Ensemble(Base):
    """
    Implementation of ensemble of configurations table.
    All types of ensembles are listed here.
    `short_tag` and `long_tag` are available to identify which type of ensembles are listed.
    """

    configurations = models.ManyToManyField(GaugeConfig)
    label = models.CharField(
        max_length=40,
        null=False,
        blank=False,
        unique=True,
        help_text="Label to identify ensemble for easy searches",
    )

    @property
    def short_tag(self) -> Optional[str]:
        """Returns the tag of the first configuration.
        """
        first = self.configurations.first()  # pylint: disable=E1101
        return first.short_tag if first else None

    @property
    def stream(self) -> Optional[str]:
        """Returns the tag of the first configuration.
        """
        first = self.configurations.first()  # pylint: disable=E1101
        return first.stream if first else None

    @property
    def long_tag(self) -> Optional[str]:
        """Returns descriptive long tag of first configuration
        """
        first = self.configurations.first()  # pylint: disable=E1101
        return first.specialization.long_tag if first else None

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        """Checks if all configurations have the same meta info.
        """
        first = data["configurations"].first()  # pylint: disable=E1101
        if first:
            for config in data["configurations"].all()[1:]:  # pylint: disable=E1101
                if not first.same_ensemble(config):
                    raise ValidationError(
                        f"{config} is from a different ensemble compared to first config {first}"
                    )
