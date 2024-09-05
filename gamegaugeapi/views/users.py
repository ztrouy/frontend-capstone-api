from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from gamegaugeapi.models import Group
from .games import GameSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "username"]
        extra_kwargs = {"password": {"write_only": True}}


class UserGroupSerializer(serializers.ModelSerializer):
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


class UserDetailedSerializer(serializers.ModelSerializer):
    isOwner = serializers.SerializerMethodField()
    games = GameSerializer(many=True, read_only=True)
    joined_groups = UserGroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "games", "joined_groups", "isOwner"]

    def get_isOwner(self, obj):
         return self.context["request"].user == obj

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["groups"] = rep.pop("joined_groups")
        return rep


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="register")
    def register_account(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                first_name="",
                last_name="",
                password=serializer.validated_data["password"]
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def user_login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token = Token.objects.get(user=user)
            return Response({"token": token.key, "valid": True}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="me")
    def auth_user(self, request):
        token_key = request.data.get("token")

        try:
            token = Token.objects.get(key=token_key)
            user = User.objects.get(id=token.user_id)
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Token.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserDetailedSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)

            if user != request.auth.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                user.username = serializer.validated_data["username"]
                user.save()

                serializer = UserSerializer(user, context={"request": request})
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
