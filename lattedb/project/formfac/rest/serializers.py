# pylint: disable=too-few-public-methods, missing-docstring, too-many-ancestors
"""This module contains the serializers for the form factor 4D models

A serializers maps a table to a JSON like file.
This json map is needed for shifting the workload of javascript tables back to the
server.
"""
from rest_framework import routers, serializers, viewsets

from lattedb.project.formfac.models import ConcatenatedFormFactor4DFile
from lattedb.project.formfac.models import DiskConcatenatedFormFactor4DFile
from lattedb.project.formfac.models import TapeConcatenatedFormFactor4DFile

from lattedb.project.formfac.models import TSlicedSAveragedFormFactor4DFile
from lattedb.project.formfac.models import DiskTSlicedSAveragedFormFactor4DFile
from lattedb.project.formfac.models import TapeTSlicedSAveragedFormFactor4DFile

from lattedb.project.formfac.models import TSlicedFormFactor4DFile
from lattedb.project.formfac.models import DiskTSlicedFormFactor4DFile

from lattedb.project.formfac.models import FormFactor4DFile
from lattedb.project.formfac.models import DiskFormFactor4DFile

from lattedb.project.formfac.models import CorrelatorMeta
from lattedb.project.formfac.models import DiskCorrelatorH5Dset
from lattedb.project.formfac.models import TapeCorrelatorH5Dset

from lattedb.project.formfac.models import TSlicedSAveragedSpectrum4DFile
from lattedb.project.formfac.models import DiskTSlicedSAveragedSpectrum4DFile
from lattedb.project.formfac.models import TapeTSlicedSAveragedSpectrum4DFile

from lattedb.project.formfac.models import TSlicedSpectrum4DFile
from lattedb.project.formfac.models import DiskTSlicedSpectrum4DFile

from lattedb.project.formfac.models import Spectrum4DFile
from lattedb.project.formfac.models import DiskSpectrum4DFile

VIEWSETS = []

# -------------------------------------
# ConcatenatedFormFactor4D
# -------------------------------------


class ConcatenatedFormFactor4DFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcatenatedFormFactor4DFile
        fields = "__all__"


class DiskConcatenatedFormFactor4DFileSerializer(serializers.ModelSerializer):
    file = ConcatenatedFormFactor4DFileSerializer()

    class Meta:
        model = DiskConcatenatedFormFactor4DFile
        fields = "__all__"


class TapeConcatenatedFormFactor4DFileSerializer(serializers.ModelSerializer):
    file = ConcatenatedFormFactor4DFileSerializer()

    class Meta:
        model = TapeConcatenatedFormFactor4DFile
        fields = "__all__"


class DiskConcatenatedFormFactor4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "disk-concat"
    exclude_from_nav = True
    queryset = DiskConcatenatedFormFactor4DFile.objects.all()
    serializer_class = DiskConcatenatedFormFactor4DFileSerializer


VIEWSETS.append(DiskConcatenatedFormFactor4DFileViewSet)


class TapeConcatenatedFormFactor4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "tape-concat"
    exclude_from_nav = True
    queryset = TapeConcatenatedFormFactor4DFile.objects.all()
    serializer_class = TapeConcatenatedFormFactor4DFileSerializer


VIEWSETS.append(TapeConcatenatedFormFactor4DFileViewSet)

# -------------------------------------
# TSlicedSAveragedFormFactor4D
# -------------------------------------


class TSlicedSAveragedFormFactor4DFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSlicedSAveragedFormFactor4DFile
        fields = "__all__"


class DiskTSlicedSAveragedFormFactor4DFileSerializer(serializers.ModelSerializer):
    file = TSlicedSAveragedFormFactor4DFileSerializer()

    class Meta:
        model = DiskTSlicedSAveragedFormFactor4DFile
        fields = "__all__"


class TapeTSlicedSAveragedFormFactor4DFileSerializer(serializers.ModelSerializer):
    file = TSlicedSAveragedFormFactor4DFileSerializer()

    class Meta:
        model = TapeTSlicedSAveragedFormFactor4DFile
        fields = "__all__"


class DiskTSlicedSAveragedFormFactor4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "disk-sliced-averaged"
    exclude_from_nav = True
    queryset = DiskTSlicedSAveragedFormFactor4DFile.objects.all()
    serializer_class = DiskTSlicedSAveragedFormFactor4DFileSerializer


VIEWSETS.append(DiskTSlicedSAveragedFormFactor4DFileViewSet)


class TapeTSlicedSAveragedFormFactor4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "tape-sliced-averaged-status"
    exclude_from_nav = True
    queryset = TapeTSlicedSAveragedFormFactor4DFile.objects.all()
    serializer_class = TapeTSlicedSAveragedFormFactor4DFileSerializer


VIEWSETS.append(TapeTSlicedSAveragedFormFactor4DFileViewSet)

# -------------------------------------
# TSlicedFormFactor4D
# -------------------------------------


class TSlicedFormFactor4DFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSlicedFormFactor4DFile
        fields = "__all__"


class DiskTSlicedFormFactor4DFileSerializer(serializers.ModelSerializer):
    file = TSlicedFormFactor4DFileSerializer()

    class Meta:
        model = DiskTSlicedFormFactor4DFile
        fields = "__all__"


class DiskTSlicedFormFactor4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "disk-sliced"
    exclude_from_nav = True
    queryset = DiskTSlicedFormFactor4DFile.objects.all()
    serializer_class = DiskTSlicedFormFactor4DFileSerializer


VIEWSETS.append(DiskTSlicedFormFactor4DFileViewSet)

# -------------------------------------
# TSlicedSAveragedFormFactor4D
# -------------------------------------


class FormFactor4DFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormFactor4DFile
        fields = "__all__"


class DiskFormFactor4DFileSerializer(serializers.ModelSerializer):
    file = FormFactor4DFileSerializer()

    class Meta:
        model = DiskFormFactor4DFile
        fields = "__all__"


class DiskFormFactor4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "disk"
    exclude_from_nav = True
    queryset = DiskFormFactor4DFile.objects.all()
    serializer_class = DiskFormFactor4DFileSerializer


VIEWSETS.append(DiskFormFactor4DFileViewSet)

# -------------------------------------
# Correlator Tables
# -------------------------------------


class CorrelatorMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrelatorMeta
        fields = "__all__"


class DiskCorrelatorH5DsetFileSerializer(serializers.ModelSerializer):
    meta = CorrelatorMetaSerializer()

    class Meta:
        model = DiskCorrelatorH5Dset
        fields = "__all__"


class DiskCorrelatorH5DsetFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "disk-correlator-h5dset"
    exclude_from_nav = True
    queryset = DiskCorrelatorH5Dset.objects.all()
    serializer_class = DiskCorrelatorH5DsetFileSerializer


VIEWSETS.append(DiskCorrelatorH5DsetFileViewSet)


class TapeCorrelatorH5DsetFileSerializer(serializers.ModelSerializer):
    meta = CorrelatorMetaSerializer()

    class Meta:
        model = TapeCorrelatorH5Dset
        fields = "__all__"


class TapeCorrelatorH5DsetFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "tape-correlator-h5dset"
    exclude_from_nav = True
    queryset = TapeCorrelatorH5Dset.objects.all()
    serializer_class = TapeCorrelatorH5DsetFileSerializer


VIEWSETS.append(TapeCorrelatorH5DsetFileViewSet)

# -------------------------------------
# Spectrum
# -------------------------------------


class TSlicedSAveragedSpectrum4DFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSlicedSAveragedSpectrum4DFile
        fields = "__all__"


class DiskTSlicedSAveragedSpectrum4DFileSerializer(serializers.ModelSerializer):
    file = TSlicedSAveragedSpectrum4DFileSerializer()

    class Meta:
        model = DiskTSlicedSAveragedSpectrum4DFile
        fields = "__all__"


class TapeTSlicedSAveragedSpectrum4DFileSerializer(serializers.ModelSerializer):
    file = TSlicedSAveragedSpectrum4DFileSerializer()

    class Meta:
        model = TapeTSlicedSAveragedSpectrum4DFile
        fields = "__all__"


class DiskTSlicedSAveragedSpectrum4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "disk-sliced-averaged"
    exclude_from_nav = True
    queryset = DiskTSlicedSAveragedSpectrum4DFile.objects.all()
    serializer_class = DiskTSlicedSAveragedSpectrum4DFileSerializer


VIEWSETS.append(DiskTSlicedSAveragedSpectrum4DFileViewSet)


class TapeTSlicedSAveragedSpectrum4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "tape-sliced-averaged-status"
    exclude_from_nav = True
    queryset = TapeTSlicedSAveragedSpectrum4DFile.objects.all()
    serializer_class = TapeTSlicedSAveragedSpectrum4DFileSerializer


VIEWSETS.append(TapeTSlicedSAveragedSpectrum4DFileViewSet)

# -------------------------------------
# TSlicedSpectrum4D
# -------------------------------------


class TSlicedSpectrum4DFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TSlicedSpectrum4DFile
        fields = "__all__"


class DiskTSlicedSpectrum4DFileSerializer(serializers.ModelSerializer):
    file = TSlicedSpectrum4DFileSerializer()

    class Meta:
        model = DiskTSlicedSpectrum4DFile
        fields = "__all__"


class DiskTSlicedSpectrum4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "disk-sliced"
    exclude_from_nav = True
    queryset = DiskTSlicedSpectrum4DFile.objects.all()
    serializer_class = DiskTSlicedSpectrum4DFileSerializer


VIEWSETS.append(DiskTSlicedSpectrum4DFileViewSet)

# -------------------------------------
# TSlicedSAveragedSpectrum4D
# -------------------------------------


class Spectrum4DFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spectrum4DFile
        fields = "__all__"


class DiskSpectrum4DFileSerializer(serializers.ModelSerializer):
    file = Spectrum4DFileSerializer()

    class Meta:
        model = DiskSpectrum4DFile
        fields = "__all__"


class DiskSpectrum4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "disk"
    exclude_from_nav = True
    queryset = DiskSpectrum4DFile.objects.all()
    serializer_class = DiskSpectrum4DFileSerializer


VIEWSETS.append(DiskSpectrum4DFileViewSet)


ROUTER = routers.DefaultRouter()
for viewset in VIEWSETS:
    ROUTER.register(viewset.name, viewset)
