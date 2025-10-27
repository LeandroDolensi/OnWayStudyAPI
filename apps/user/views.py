from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from apps.user.models import User
from apps.user.serializers import UserSerializer
from security.authentication import OnWayStudyBaseAuthentication


class UserViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "nickname"
    authentication_classes = [OnWayStudyBaseAuthentication]
