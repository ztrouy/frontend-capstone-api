from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from gamegaugeapi.models import Platform


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ["id", "name"]


class PlatformViewSet(viewsets.ViewSet):
    def list(self, request):
        platforms = Platform.objects.all()
        serializer = PlatformSerializer(platforms, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            platform = Platform.objects.get(pk=pk)
            serializer = PlatformSerializer(platform, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Platform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
