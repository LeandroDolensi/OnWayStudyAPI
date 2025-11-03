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
