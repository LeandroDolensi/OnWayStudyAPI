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
from django.http import Http404


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

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            self.kwargs["id"] = self.kwargs[self.lookup_field]
            self.lookup_field = "id"
            return super().get_object()
