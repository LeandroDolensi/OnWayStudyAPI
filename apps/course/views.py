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
    serializer_class = CourseSerializer
    lookup_field = "name"
    extra_lookup_field = "acronym"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        self.queryset = Course.objects.filter(
            institution__in=self.request.user.institutions.all()
        )
        return super().get_queryset()
