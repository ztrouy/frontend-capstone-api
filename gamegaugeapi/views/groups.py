from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from gamegaugeapi.models import Group


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


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
