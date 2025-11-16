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
    """
    A ViewSet for handling CRUD operations on User instances.

    This ViewSet provides endpoints for creating, retrieving, updating,
    and deleting users. It ensures that users can only access their own data.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        """
        Retrieves the queryset of users filtered by the current user's ID.

        This method ensures that a user can only view their own user object.

        Returns:
            QuerySet: A queryset containing only the current user.
        """
        self.queryset = User.objects.filter(id=self.request.user.id)
        return super().get_queryset()
