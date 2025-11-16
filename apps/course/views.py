from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from apps.course.models import Course
from apps.course.serializers import CourseSerializer
from security.authentication import OnWayStudyBaseAuthentication


class CourseViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    """
    A ViewSet for handling CRUD operations on Course instances.

    This ViewSet provides endpoints for creating, retrieving, updating,
    and deleting courses. It ensures that users can only access courses
    related to their own institutions.
    """

    serializer_class = CourseSerializer
    lookup_field = "id"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        """
        Retrieves the queryset of courses filtered by the user's institutions.

        This method ensures that users can only view courses that belong to
        institutions they are associated with.

        Returns:
            QuerySet: A queryset of Course instances.
        """
        self.queryset = Course.objects.filter(
            institution__in=self.request.user.institutions.all()
        )
        return super().get_queryset()
