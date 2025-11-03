from rest_framework.serializers import SlugRelatedField
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
