from rest_framework.serializers import SlugRelatedField, ModelSerializer
from apps.activity.models import Activity
from apps.discipline.models import Discipline
from django_libs.custom_serializer import CustomModelSerializer


class ActivitySerializer(CustomModelSerializer):
    """
    Serializer for the Activity model.

    This serializer handles the serialization and deserialization of Activity
    instances, ensuring that the `discipline` field is correctly handled
    and that the queryset for disciplines is filtered based on the user.
    """

    discipline = SlugRelatedField(slug_field="id", queryset=Discipline.objects.all())

    class Meta:
        model = Activity
        fields = [
            "id",
            "name",
            "status",
            "grade_weight",
            "expected_grade",
            "grade_result",
            "delivery_date",
            "discipline",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        """
        Initializes the ActivitySerializer.

        This method filters the queryset for the `discipline` field to only
        include disciplines that belong to the current user.
        """
        super().__init__(*args, **kwargs)
        self.fields["discipline"].queryset = Discipline.objects.filter(
            course__institution__user=self._get_user()
        )

    def create(self, validated_data):
        """
        Creates a new Activity instance.

        Args:
            validated_data (dict): The validated data for the new activity.

        Returns:
            Activity: The newly created Activity instance.
        """
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing Activity instance.

        Args:
            instance (Activity): The existing Activity instance.
            validated_data (dict): The validated data for the update.

        Returns:
            Activity: The updated Activity instance.
        """
        return super().update(instance, validated_data)

    def _calculate_expected_grade(self, validated_data):
        pass


class DisciplineActivitySerializer(ModelSerializer):
    """
    Serializer for the Activity model, for use within Discipline serialization.

    This serializer provides a read-only representation of activities
    to be nested within the Discipline serializer.
    """

    class Meta:
        model = Activity
        fields = [
            "id",
            "name",
            "status",
            "grade_weight",
            "expected_grade",
            "grade_result",
            "delivery_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
