"""Script which checks status of existing baryon 2pt correlators
"""
import os
import logging

from h5py import File

from django.db import transaction

from tqdm import tqdm

from lattedb.correlator.models import Baryon2pt
from lattedb.status.models.correlator import Baryon2pt as Baryon2ptStatus

LOGGER = logging.getLogger("base")
LOGGER.setLevel(logging.INFO)

HOME = "summit"
ROOT_PATH = {
    "a09m310_e": "/ccs/proj/lgt100/c51/x_files/project_2/production/a09m310_e/data"
}


@transaction.atomic
def check_status(status: Baryon2ptStatus, root_path: str):
    """Checks status of baryon2pt correlator.

    The logic works as follows:

    **Arguments**
        baryon2pt: Baryon2pt
            The meta information database object of the correlator

        root_path: str
            The root path on the host where to expect the correlator.
    """
    baryon2pt = status.baryon2pt
    LOGGER.debug("Checking status of %s", baryon2pt)

    file_path = status.file_path or os.path.join(
        root_path, f"{baryon2pt.short_tag}_{baryon2pt.n_config}.h5"
    )
    dset_path = status.dset_path or get_dset_path(baryon2pt)
    LOGGER.debug("Looking up file %s and dset path %s", file_path, dset_path)

    if os.path.exists(file_path) and data_exist(file_path, dset_path):
        LOGGER.debug("Data was found. Updating status")
        status.status = 2  # data exists
        status.file_path = file_path
        status.dset_path = dset_path
    else:
        LOGGER.debug("Data was not found. Updating status")
        status.status = 0  # data unknown
        status.file_path = None
        status.dset_path = None

    status.save()


def get_dset_path(baryon2pt: Baryon2pt) -> str:
    """Parses the hdf5 path for a baryon2pt correlator
    """
    prop = baryon2pt.propagator0
    config = prop.gaugeconfig
    src = baryon2pt.source
    return os.path.join(
        (
            f"gf{config.gaugesmear.flowtime:1.1f}"
            "_"
            f"w{src.wavefunctionsmear.radius:1.1f}"
            "_"
            f"n{src.wavefunctionsmear.step}"
            "_"
            f"M5{prop.fermionaction.m5:1.1f}"
            "_"
            f"L5{int(prop.fermionaction.l5)}"
            "_"
            f"a{prop.fermionaction.specialization.alpha5:1.1f}"
        ).replace(".", "p"),
        "spectrum",
        f"ml{prop.fermionaction.quark_mass}".replace(".", "p").rstrip("0"),
        f"{baryon2pt.tag}" + ("" if src.parity else "_np"),
        "spin_" + ("up" if src.spin_x2 else "dn"),
        f"x{prop.origin_x}y{prop.origin_y}z{prop.origin_z}t{prop.origin_t}",
    )


def data_exist(file_path: str, dset_path: str) -> bool:
    """Checks if `dset_path` is contained in `file_path`.

    **Arguments**
        file_path: str
            Path to HDF5 file

        dset_path: str
            Path to data set in HDF5 file.
    """
    with File(file_path, "r") as h5f:
        return dset_path in h5f


def prepopulate_status():
    """Creates status unknown for all Baryon2pt correlators (for faster updates)
    """
    no_status_2pts = Baryon2pt.objects.exclude(
        id__in=Baryon2ptStatus.objects.values_list("baryon2pt__id")
    )
    Baryon2ptStatus.objects.bulk_create(
        [
            Baryon2ptStatus(baryon2pt=baryon2pt, home=HOME, status=0)
            for baryon2pt in no_status_2pts
        ]
    )


@transaction.atomic
def mark_unknown(status: Baryon2ptStatus):
    """Marks status of correlator unknown
    """
    status.status = 0
    status.save()


def main():
    """Looks up Baryon2pt correlators from the meta information and checks their status.
    """
    LOGGER.info("Start scaning for existing baryon 2pt correlators by ensemble")

    prepopulate_status()

    for status in tqdm(Baryon2ptStatus.objects.all()):
        LOGGER.debug("Looking for status of %s", status.baryon2pt)
        descriptor = f"{status.baryon2pt.short_tag}_{status.baryon2pt.stream}"
        root_path = ROOT_PATH.get(descriptor, None)

        if root_path is not None:
            check_status(status, root_path)

        else:
            LOGGER.debug("No path specified for ensemble %s.", descriptor)
            mark_unknown(status)


if __name__ == "__main__":
    main()
