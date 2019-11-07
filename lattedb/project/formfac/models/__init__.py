"""Imports all models from the formfac.models submodules
"""

# from lattedb.project.formfac.models.data.ff4d import (
#     FormFactor4DFile,
#     DiskFormFactor4DFile,
# )
from lattedb.project.formfac.models.data.tsliced_ff4d import (
    TSlicedFormFactor4DFile,
    DiskTSlicedFormFactor4DFile,
)
from lattedb.project.formfac.models.data.tsliced_savged_ff4d import (
    TSlicedSAveragedFormFactor4DFile,
    DiskTSlicedSAveragedFormFactor4DFile,
    TapeTSlicedSAveragedFormFactor4DFile,
)
from lattedb.project.formfac.models.data.concatenated_ff4d import (
    ConcatenatedFormFactor4DFile,
    DiskConcatenatedFormFactor4DFile,
    TapeConcatenatedFormFactor4DFile,
)
