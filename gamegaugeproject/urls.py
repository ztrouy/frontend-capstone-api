from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from gamegaugeapi.views import UserViewSet, GenreViewSet, PlatformViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"genres", GenreViewSet, "genre")
router.register(r"platforms", PlatformViewSet, "platform")

urlpatterns = [
    path('', include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path("register", UserViewSet.as_view({"post": "register_account"}), name="register"),
    path("me", UserViewSet.as_view({"post": "auth_user"}), name="me")
]

