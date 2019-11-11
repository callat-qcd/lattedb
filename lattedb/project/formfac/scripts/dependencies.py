"""Script which checks dependencies for all form factor models
"""
from typing import Optional

from logging import getLogger

from tqdm import tqdm

from lattedb.project.formfac.models import FormFactor4DFile, TSlicedFormFactor4DFile

LOGGER = getLogger("espressodb")


def update_ff_dependencies(update_all: bool = False, batch_size: Optional[int] = None):
    """Iterates over form factor files and updates the dependent information.

    First gathers information and runs buld update afterwards.

    Arguments:
        update_all:
            If True, update all Form Factor entries. Defaults to updating only entries
            where the `dependent` information is missing.
        batch_size:
            Batch size for bulk update. Defaults to all at once.
    """
    LOGGER.info("Start updating dependnts of form factor files.")
    if update_all:
        ffs = FormFactor4DFile.objects.all()
    else:
        ffs = FormFactor4DFile.objects.filter(dependent__isnull=True)
    LOGGER.info("Will updated %d files.", ffs.count())

    tffs = TSlicedFormFactor4DFile.objects.all()

    ffs_for_update = []
    for ff in tqdm(ffs):
        query = {
            key: getattr(ff, key)
            for key in [
                "ensemble",
                "stream",
                "source_set",
                "configuration",
                "t_separation",
            ]
        }
        tff = tffs.filter(**query)
        if tff.count() == 1:
            ff.dependent = tff.first()
            ffs_for_update.append(ff)

    LOGGER.info(
        "Found %d/%d dependents. Starting bulk update.",
        len(ffs_for_update),
        ffs.count(),
    )
    FormFactor4DFile.objects.bulk_update(
        ffs_for_update, ["dependent"], batch_size=batch_size
    )
    LOGGER.info("Done.")


def main():
    """Updates all missing dependencies of form factor files
    """
    update_ff_dependencies()


if __name__ == "__main__":
    main()
