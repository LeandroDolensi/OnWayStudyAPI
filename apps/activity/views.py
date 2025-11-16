from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from apps.activity.models import Activity
from apps.activity.serializers import ActivitySerializer
from apps.course.models import Course
from apps.discipline.models import Discipline
from security.authentication import OnWayStudyBaseAuthentication
from rest_framework import status
from rest_framework.response import Response
from apps.discipline.service import DisciplineService


class ActivityViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    """
    A ViewSet for handling CRUD operations on Activity instances.

    This ViewSet provides endpoints for creating, retrieving, updating,
    and deleting activities. It ensures that users can only access
    activities related to their own institutions and courses.
    """

    serializer_class = ActivitySerializer
    lookup_field = "id"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        """
        Retrieves the queryset of activities filtered by the user's institutions.

        This method ensures that users can only view activities that belong to
        disciplines within courses they are enrolled in.

        Returns:
            QuerySet: A queryset of Activity instances.
        """
        filtered_user_courses = Course.objects.filter(
            institution__in=self.request.user.institutions.all()
        )
        filtered_user_disciplines = Discipline.objects.filter(
            course__in=filtered_user_courses.all()
        )
        self.queryset = Activity.objects.filter(
            discipline__in=filtered_user_disciplines
        )
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of a new activity.

        After creating the activity, it triggers an update of the expected
        grades for the associated discipline.

        Args:
            request (Request): The request object containing the activity data.

        Returns:
            Response: A response with the serialized activity data and a 201 status code.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = serializer.instance
        discipline = instance.discipline
        discipline_service = DisciplineService(discipline)
        discipline_service.update_expected_grades()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        Handles the update of an existing activity.

        This method updates the activity and then recalculates the expected
        grades for both the old and new disciplines if the discipline was changed.

        Args:
            request (Request): The request object containing the updated activity data.

        Returns:
            Response: A response with the serialized activity data.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        old_discipline = instance.discipline

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        new_discipline = serializer.instance.discipline

        new_discipline_service = DisciplineService(new_discipline)
        new_discipline_service.update_expected_grades()

        if old_discipline != new_discipline:
            old_discipline_service = DisciplineService(old_discipline)
            old_discipline_service.update_expected_grades()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Handles the deletion of an activity.

        After deleting the activity, it triggers an update of the expected
        grades for the associated discipline.

        Args:
            request (Request): The request object.

        Returns:
            Response: A response with a 204 status code.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        discipline = instance.discipline
        discipline_service = DisciplineService(discipline)
        discipline_service.update_expected_grades()
        return Response(status=status.HTTP_204_NO_CONTENT)
