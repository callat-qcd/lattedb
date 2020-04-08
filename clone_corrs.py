"""This script clones correlators to and from the local db to the psql db.

I assume you run this script on ithems where the default db (`db-config.yaml`) is
set up for ithems and the local db (`db-config-local.yaml`) is a SQLite db.

Note: for this dumping to work, one has to dump stuff in the right order to not violate
Foreign Key constraints. For example, if you dump a tape file before the meta exists,
the tape file complains that there is no associated meta present.
"""
from argparse import ArgumentParser

from collections import OrderedDict

from tqdm import tqdm

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
from django.db.models import ManyToManyRel, ManyToOneRel

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
PARSER.add_argument(
    "-u",
    dest="update",
    action="store_true",
    help="Populate default database from local database.",
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


def assert_queryset_equal(qs1, qs2):
    """Compares two querysets and checks if all rows and columns are equal

    Ignores ManyToManyRel, ManyToOneRel and last_modified
    """
    # Check if same count
    assert qs1.count() == qs2.count()
    # Check if same ids
    assert sorted(qs1.values_list("id")) == sorted(qs2.values_list("id"))
    # Check if all columns are the same
    for obj1, obj2 in tqdm(list(zip(qs1.order_by("-id"), qs2.order_by("-id")))):
        for field in obj1._meta.get_fields():
            if (
                isinstance(field, (ManyToManyRel, ManyToOneRel))
                or field.name == "last_modified"
            ):
                continue
            if not getattr(obj1, field.name) == getattr(obj2, field.name):
                raise AssertionError(f"{obj1} != {obj2}\nfield: {field}")


def update_default_from_local():
    """
    """
    new_local_objects = OrderedDict()
    # First check that all the data present on default is also present on local
    print("Checking consistency")
    for Model in [User, CorrelatorMeta, DiskCorrelatorH5Dset, TapeCorrelatorH5Dset]:
        print("\t*", Model)
        # Store data in default db
        default_objects = Model.objects.all()
        local_objects = Model.objects.using("local").filter(
            pk__in=list(default_objects.values_list("pk", flat=True))
        )
        assert_queryset_equal(default_objects, local_objects)
        new_local_objects[Model] = (
            Model.objects.using("local").all().difference(local_objects)
        )

    print("Now updating default with new objects")
    print(
        "\n".join(
            [f"\t* {key}: {val.count()}" for key, val in new_local_objects.items()]
        )
    )
    go_on = input("Continue (y/N):")
    if not go_on.lower() == "y":
        raise KeyboardInterrupt()

    # Insert data atomic in new db
    with transaction.atomic():
        for Model, objects in new_local_objects.items():
            # Can use bulk create because objects don't exist
            Model.objects.bulk_create(objects)

    print("Done")


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
        return

    if args.update:
        print(
            "Updating default database {default} from local database {local}.".format(
                local=DATABASES["local"]["NAME"], default=DATABASES["default"]["NAME"]
            )
        )
        update_default_from_local()


if __name__ == "__main__":
    main()
