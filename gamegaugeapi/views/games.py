from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from gamegaugeapi.models import Game, Genre, Platform
from .genres import GenreSerializer
from .platforms import PlatformSerializer


class GameSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    platforms = PlatformSerializer(many=True)
    isOwned = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ["id", "name", "max_players", "image_header", "genres", "platforms", "isOwned"]

    def get_isOwned(self, obj):
        user = self.context["request"].user
        return obj.usergame_set.filter(user=user).exists()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["maxPlayers"] = rep.pop("max_players")
        rep["imageHeader"] = rep.pop("image_header")
        return rep


class GameViewSet(viewsets.ViewSet):
    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        game = Game.objects.create(
            name = request.data.get("name"),
            max_players = request.data.get("maxPlayers"),
            image_header = request.data.get("imageHeader")
        )

        genre_ids = request.data.get("genres", [])
        game.genres.set(genre_ids)

        platform_ids = request.data.get("platforms", [])
        game.platforms.set(platform_ids)

        serializer = GameSerializer(game, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
