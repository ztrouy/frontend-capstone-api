from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from gamegaugeapi.models import Group
from .users import UserSerializer
from .games import GameSerializer


class GroupSerializer(serializers.ModelSerializer):
    isMember = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ["id", "name", "isMember", "memberCount"]

    def get_isMember(self, obj):
        user = self.context["request"].user
        return obj.members.filter(id=user.id).exists()

    def get_memberCount(self, obj):
        return obj.members.count()


class GroupDetailedSerializer(serializers.ModelSerializer):
    isMember = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()
    games = serializers.SerializerMethodField()
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "members", "memberCount", "games", "isMember"]

    def get_isMember(self, obj):
        user = self.context["request"].user
        return obj.members.filter(id=user.id).exists()

    def get_memberCount(self, obj):
        return obj.members.count()

    def get_games(self, obj):
        games = obj.get_common_games()
        return GameSerializer(games, many=True, context={"request": self.context["request"]}).data


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupDetailedSerializer(group, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
