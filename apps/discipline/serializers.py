from rest_framework.serializers import SlugRelatedField, ModelSerializer
from apps.activity.serializers import DisciplineActivitySerializer
from apps.discipline.models import Discipline
from django_libs.custom_serializer import CustomModelSerializer
from apps.course.models import Course


class DisciplineSerializer(CustomModelSerializer):
    course = SlugRelatedField(slug_field="id", queryset=Course.objects.all())

    class Meta:
        model = Discipline
        fields = [
            "id",
            "name",
            "extra_information",
            "semester",
            "final_grade",
            "final_result",
            "course",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(
            institution__user=self._get_user()
        )


class CourseDisciplineSerializer(ModelSerializer):
    activities = DisciplineActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Discipline
        fields = [
            "id",
            "name",
            "extra_information",
            "semester",
            "final_grade",
            "final_result",
            "created_at",
            "updated_at",
            "activities",
        ]
        read_only_fields = fields
