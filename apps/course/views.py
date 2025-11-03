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
from django.http import Http404


class CourseViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    serializer_class = CourseSerializer
    lookup_field = "name"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        self.queryset = Course.objects.filter(
            institution__in=self.request.user.institutions.all()
        )
        return super().get_queryset()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            self.kwargs["acronym"] = self.kwargs[self.lookup_field]
            self.lookup_field = "acronym"
            try:
                return super().get_object()
            except Http404:
                self.kwargs["id"] = self.kwargs[self.lookup_field]
                self.lookup_field = "id"
                return super().get_object()
