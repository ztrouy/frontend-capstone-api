from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
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


class GameUpdateSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
    platforms = serializers.PrimaryKeyRelatedField(many=True, queryset=Platform.objects.all())

    class Meta:
        model = Game
        fields = ["id", "name", "max_players", "image_header", "genres", "platforms"]

    def to_internal_value(self, data):
        data = {
            "id": data.get("id"),
            "name": data.get("name"),
            "max_players": data.get("maxPlayers"),
            "image_header": data.get("imageHeader"),
            "genres": data.get("genres"),
            "platforms": data.get("platforms")
        }
        return super().to_internal_value(data)


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

    def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)

            serializer = GameUpdateSerializer(game, data=request.data)
            if serializer.is_valid():
                game.name = serializer.validated_data["name"]
                game.max_players = serializer.validated_data["max_players"]
                game.image_header = serializer.validated_data["image_header"]
                game.save()

                genre_ids = request.data.get("genres", [])
                game.genres.set(genre_ids)

                platform_ids = request.data.get("platforms", [])
                game.platforms.set(platform_ids)

                serializer = GameSerializer(game, context={"request": request})
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"], url_path="own")
    def own_game(self, request, pk=None):
        user = request.auth.user
        try:
            game = Game.objects.get(pk=pk)
            if user.usergame_set.filter(game=game).exists():
                return Response({"details": "You already own this game"}, status=status.HTTP_400_BAD_REQUEST)

            user.games.add(game.id)
            return Response(status=status.HTTP_201_CREATED)

        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)