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
from security.permissions import IsOwner
from rest_framework.permissions import AllowAny


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

    def get_permissions(self):
        """
        The only method available to the public user is to create a new user.
        In other words, authentication is not required to create a new user.
        """
        permission_classes = [AllowAny]
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]
