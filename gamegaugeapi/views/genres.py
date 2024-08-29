from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from gamegaugeapi.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class GenreViewSet(viewsets.ViewSet):
    def list(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Genre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
