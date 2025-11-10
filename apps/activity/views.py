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
    serializer_class = ActivitySerializer
    lookup_field = "id"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
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
        instance = self.get_object()
        self.perform_destroy(instance)
        discipline = instance.discipline
        discipline_service = DisciplineService(discipline)
        discipline_service.update_expected_grades()
        return Response(status=status.HTTP_204_NO_CONTENT)
