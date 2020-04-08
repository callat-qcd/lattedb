"""This script clones correlators to and from the local db to the psql db.

I assume you run this script on ithems where the default db (`db-config.yaml`) is
set up for ithems and the local db (`db-config-local.yaml`) is a SQLite db.

Note: for this dumping to work, one has to dump stuff in the right order to not violate
Foreign Key constraints. For example, if you dump a tape file before the meta exists,
the tape file complains that there is no associated meta present.
"""
from argparse import ArgumentParser

from collections import OrderedDict

from lattedb.config.settings import DATABASES
from lattedb.project.formfac.models.data.correlator import (
    CorrelatorMeta,
    DiskCorrelatorH5Dset,
    TapeCorrelatorH5Dset,
)

# Need to import lattedb first to set up django project
# pylint: disable=C0411

from django.contrib.auth.models import User
from django.db import transaction

PARSER = ArgumentParser(
    description="Script allows to export all data to and from default"
    " database (postgres) to local database (SQL)."
)

PARSER.add_argument(
    "-n",
    dest="new",
    action="store_true",
    help="Populate new local database from default. Local must be empty.",
)


def validate_dbs():
    """Checks if the DBs are properly configured
    """
    if "default" not in DATABASES or "local" not in DATABASES:
        raise KeyError("Could not identify local and default db.")


def create_new_local_from_default():
    """This dumps all relevant correlator data from the default DB to the local db.

    Assumes local db is empty
    """
    default_data = OrderedDict()

    # First check local is empty
    for Model in [User, CorrelatorMeta, DiskCorrelatorH5Dset, TapeCorrelatorH5Dset]:
        if Model.objects.using("local").count() > 0:
            raise ValueError(f"Model {Model} has entries in local db. Abort.")

        # Store data in default db
        default_data[Model] = Model.objects.all()

    # Insert data atomic in new db
    with transaction.atomic():
        for Model, objects in default_data.items():
            # Can use bulk create because objects don't exist
            Model.objects.using("local").bulk_create(objects)


def main():
    """Runs the copy scripts
    """
    args = PARSER.parse_args()
    validate_dbs()

    if args.new:
        print(
            "Populating new local database {local} from default {default}.".format(
                local=DATABASES["local"]["NAME"], default=DATABASES["default"]["NAME"]
            )
        )
        create_new_local_from_default()


if __name__ == "__main__":
    main()
