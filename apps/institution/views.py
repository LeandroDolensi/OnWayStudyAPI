from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from apps.institution.models import Institution
from apps.institution.serializers import InstitutionSerializer
from security.authentication import OnWayStudyBaseAuthentication


class InstitutionViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    serializer_class = InstitutionSerializer
    lookup_field = "name"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        self.queryset = Institution.objects.filter(user=self.request.user)
        return super().get_queryset()
