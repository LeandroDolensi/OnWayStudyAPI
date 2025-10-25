from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.user.views import UserViewSet

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
