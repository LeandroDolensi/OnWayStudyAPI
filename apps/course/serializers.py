from rest_framework.serializers import SlugRelatedField
from apps.discipline.serializers import CourseDisciplineSerializer
from apps.institution.models import Institution
from django_libs.custom_serializer import CustomModelSerializer
from apps.course.models import Course
from rest_framework.serializers import ModelSerializer


class CourseSerializer(CustomModelSerializer):
    """
    Serializer for the Course model.

    This serializer handles the serialization and deserialization of Course
    instances, ensuring that the `institution` field is correctly handled
    and that the queryset for institutions is filtered based on the user.
    """

    institution = SlugRelatedField(slug_field="id", queryset=Institution.objects.all())

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
        """
        Initializes the CourseSerializer.

        This method filters the queryset for the `institution` field to only
        include institutions that belong to the current user.
        """
        super().__init__(*args, **kwargs)
        self.fields["institution"].queryset = Institution.objects.filter(
            user=self._get_user()
        )


class InstitutionCourseSerializer(ModelSerializer):
    """
    Serializer for the Course model, for use within Institution serialization.

    This serializer provides a read-only representation of courses, including
    their disciplines, to be nested within the Institution serializer.
    """

    disciplines = CourseDisciplineSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "acronym", "created_at", "updated_at", "disciplines"]
        read_only_fields = fields
