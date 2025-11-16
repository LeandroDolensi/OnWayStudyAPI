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
    """
    A ViewSet for handling CRUD operations on Institution instances.

    This ViewSet provides endpoints for creating, retrieving, updating,
    and deleting institutions. It ensures that users can only access
    institutions that they own.
    """

    serializer_class = InstitutionSerializer
    lookup_field = "id"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        """
        Retrieves the queryset of institutions filtered by the current user.

        This method ensures that users can only view institutions that belong to them.

        Returns:
            QuerySet: A queryset of Institution instances.
        """
        self.queryset = Institution.objects.filter(user=self.request.user)
        return super().get_queryset()
