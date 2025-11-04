from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
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
    ListModelMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        self.queryset = User.objects.filter(id=self.request.user.id)
        return super().get_queryset()
