from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from gamegaugeapi.models import Game
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
