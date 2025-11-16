from rest_framework.serializers import SlugRelatedField, ModelSerializer
from apps.activity.serializers import DisciplineActivitySerializer
from apps.discipline.models import Discipline
from django_libs.custom_serializer import CustomModelSerializer
from apps.course.models import Course


class DisciplineSerializer(CustomModelSerializer):
    """
    Serializer for the Discipline model.

    This serializer handles the serialization and deserialization of Discipline
    instances, ensuring that the `course` field is correctly handled
    and that the queryset for courses is filtered based on the user.
    """

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
        """
        Initializes the DisciplineSerializer.

        This method filters the queryset for the `course` field to only
        include courses that belong to the current user.
        """
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(
            institution__user=self._get_user()
        )


class CourseDisciplineSerializer(ModelSerializer):
    """
    Serializer for the Discipline model, for use within Course serialization.

    This serializer provides a read-only representation of disciplines,
    including their activities, to be nested within the Course serializer.
    """

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
