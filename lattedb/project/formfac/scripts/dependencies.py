"""Script which checks dependencies for all form factor models
"""
from typing import Optional

from logging import getLogger

from tqdm import tqdm

from lattedb.project.formfac.models import (
    FormFactor4DFile,
    TSlicedFormFactor4DFile,
    TSlicedSAveragedFormFactor4DFile,
)

LOGGER = getLogger("espressodb")


class DepencyUpdater:  # pylint: disable=R0903
    """Class provides interface for depency->dependet bulk updates.
    """

    def __init__(self, depency, dependet, keys):
        self.depency = depency
        self.dependet = dependet
        self.keys = keys

    def update(self, update_all: bool = False, batch_size: Optional[int] = None):
        """Iterates over depency files and updates the dependent information.

        First gathers information and runs bulk update afterwards.

        Arguments:
            update_all:
                If True, update all depency entries. Defaults to updating only entries
                where the `dependent` information is missing.
            batch_size:
                Batch size for bulk update. Defaults to all at once.
        """
        LOGGER.info(
            "Start updating class dependent information of %s->%s.",
            self.depency,
            self.dependet,
        )
        LOGGER.info("Using the keys %s to uniquely identify dependents.", self.keys)
        if update_all:
            dependencies = self.depency.objects.all()
        else:
            dependencies = self.depency.objects.filter(dependent__isnull=True)
        LOGGER.info("Try to updated %d files.", dependencies.count())

        dependents = self.dependet.objects.all()

        dependencies_for_update = []
        LOGGER.info("Identifying dependents (no insert yet).")
        counter = 0
        created = 0
        for dependency in tqdm(dependencies):
            query = {key: getattr(dependency, key) for key in self.keys}
            filtered_dependents = dependents.filter(**query)

            if filtered_dependents.count() == 1:
                dependency.dependent = filtered_dependents.first()
                dependencies_for_update.append(dependency)
                counter += 1

                if batch_size and counter % batch_size == 0:
                    LOGGER.debug(
                        "Batch push to db for %d entries", len(dependencies_for_update)
                    )
                    self.depency.objects.bulk_update(
                        dependencies_for_update, ["dependent"], batch_size=batch_size
                    )
                    created += len(dependencies_for_update)
                    dependencies_for_update = []

        LOGGER.debug("Push to db for %d entries", len(dependencies_for_update))
        self.depency.objects.bulk_update(
            dependencies_for_update, ["dependent"], batch_size=batch_size
        )
        created += len(dependencies_for_update)
        LOGGER.info(
            "Found %d/%d dependents. Starting bulk update.",
            created,
            dependencies.count(),
        )
        LOGGER.info("Done.")


def main():
    """Updates all missing dependencies of form factor files
    """
    DepencyUpdater(
        FormFactor4DFile,
        dependet=TSlicedFormFactor4DFile,
        keys=[
            "ensemble",
            "stream",
            "source_set",
            "configuration",
            "t_separation",
            "source",
        ],
    ).update(batch_size=10000)

    DepencyUpdater(
        TSlicedFormFactor4DFile,
        dependet=TSlicedSAveragedFormFactor4DFile,
        keys=["ensemble", "stream", "source_set", "configuration", "t_separation",],
    ).update(batch_size=10000)


if __name__ == "__main__":
    main()
