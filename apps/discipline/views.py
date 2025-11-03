from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from apps.course.models import Course
from apps.discipline.models import Discipline
from apps.discipline.serializers import DisciplineSerializer
from security.authentication import OnWayStudyBaseAuthentication


class DisciplineViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    serializer_class = DisciplineSerializer
    lookup_field = "id"
    authentication_classes = [OnWayStudyBaseAuthentication]

    def get_queryset(self):
        filtered_user_courses = Course.objects.filter(
            institution__in=self.request.user.institutions.all()
        )
        self.queryset = Discipline.objects.filter(course__in=filtered_user_courses)
        return super().get_queryset()
