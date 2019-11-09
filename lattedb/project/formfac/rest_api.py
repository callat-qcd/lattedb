from lattedb.project.formfac.models import DiskConcatenatedFormFactor4DFile
from lattedb.project.formfac.models import ConcatenatedFormFactor4DFile
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class ConcatenatedFormFactor4DFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcatenatedFormFactor4DFile
        fields = ["id", "ensemble"]


# Serializers define the API representation.
class DiskConcatenatedFormFactor4DFileSerializer(serializers.ModelSerializer):
    file = ConcatenatedFormFactor4DFileSerializer()

    class Meta:
        model = DiskConcatenatedFormFactor4DFile
        fields = [
            "file",
            "exists",
            "machine",
            "size",
            "date_modified",
        ]


# ViewSets define the view behavior.
class DiskConcatenatedFormFactor4DFileViewSet(viewsets.ModelViewSet):
    queryset = DiskConcatenatedFormFactor4DFile.objects.all()
    serializer_class = DiskConcatenatedFormFactor4DFileSerializer


# ViewSets define the view behavior.
# class ConcatenatedFormFactor4DFileViewSet(viewsets.ModelViewSet):
#     queryset = ConcatenatedFormFactor4DFile.objects.all()
#     serializer_class = ConcatenatedFormFactor4DFileSerializer


# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()
ROUTER.register(
    r"DiskConcatenatedFormFactor4DFile", DiskConcatenatedFormFactor4DFileViewSet
)
# ROUTER.register(r"ConcatenatedFormFactor4DFile", ConcatenatedFormFactor4DFileViewSet)
