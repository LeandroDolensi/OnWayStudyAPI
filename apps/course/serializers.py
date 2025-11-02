from rest_framework.serializers import SlugRelatedField
from apps.institution.models import Institution
from django_libs.custom_serializer import CustomModelSerializer
from apps.course.models import Course


class CourseSerializer(CustomModelSerializer):
    institution = SlugRelatedField(
        slug_field="name", queryset=Institution.objects.all()
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "acronym",
            "semesters",
            "institution",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["institution"].queryset = Institution.objects.filter(
            user=self._get_user()
        )
