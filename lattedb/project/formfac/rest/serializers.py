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


VIEWSETS = []


## ConcatenatedFormFactor4D


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
    queryset = DiskConcatenatedFormFactor4DFile.objects.all()
    serializer_class = DiskConcatenatedFormFactor4DFileSerializer


VIEWSETS.append(DiskConcatenatedFormFactor4DFileViewSet)


class TapeConcatenatedFormFactor4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "tape-concat"
    queryset = TapeConcatenatedFormFactor4DFile.objects.all()
    serializer_class = TapeConcatenatedFormFactor4DFileSerializer


VIEWSETS.append(TapeConcatenatedFormFactor4DFileViewSet)

## TSlicedSAveragedFormFactor4D


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
    queryset = DiskTSlicedSAveragedFormFactor4DFile.objects.all()
    serializer_class = DiskTSlicedSAveragedFormFactor4DFileSerializer


VIEWSETS.append(DiskTSlicedSAveragedFormFactor4DFileViewSet)


class TapeTSlicedSAveragedFormFactor4DFileViewSet(viewsets.ReadOnlyModelViewSet):
    name = "tape-sliced-averaged-status"
    queryset = TapeTSlicedSAveragedFormFactor4DFile.objects.all()
    serializer_class = TapeTSlicedSAveragedFormFactor4DFileSerializer


VIEWSETS.append(TapeTSlicedSAveragedFormFactor4DFileViewSet)

## TSlicedFormFactor4D


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
    queryset = DiskTSlicedFormFactor4DFile.objects.all()
    serializer_class = DiskTSlicedFormFactor4DFileSerializer


VIEWSETS.append(DiskTSlicedFormFactor4DFileViewSet)


## TSlicedSAveragedFormFactor4D


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
    queryset = DiskFormFactor4DFile.objects.all()
    serializer_class = DiskFormFactor4DFileSerializer


VIEWSETS.append(DiskFormFactor4DFileViewSet)


ROUTER = routers.DefaultRouter()
for viewset in VIEWSETS:
    ROUTER.register(viewset.name, viewset)
