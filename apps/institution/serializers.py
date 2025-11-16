from apps.course.serializers import InstitutionCourseSerializer
from apps.institution.models import Institution
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django_libs.custom_serializer import CustomModelSerializer
from rest_framework.serializers import ModelSerializer
from environment import get_timezone


class InstitutionSerializer(CustomModelSerializer):
    """
    Serializer for the Institution model.

    This serializer handles the serialization and deserialization of Institution
    instances, including assigning the user and handling potential
    integrity errors on creation.
    """

    class Meta:
        model = Institution
        fields = ["id", "name", "user", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]
        extra_kwargs = {
            "user": {
                "validators": [],
            },
        }

    def create(self, validated_data):
        """
        Creates a new Institution instance.

        This method assigns the current user to the institution and handles
        potential IntegrityError if the institution name already exists for the user.

        Args:
            validated_data (dict): The validated data for the new institution.

        Returns:
            Institution: The newly created Institution instance.
        """
        validated_data["user"] = self._get_user()

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(
                f"The Institution name {validated_data.get("name", "")} alread exist."
            )

    def update(self, instance, validated_data):
        """
        Updates an existing Institution instance.

        This method removes the `user` field from the validated data to prevent
        it from being updated and sets the `updated_at` timestamp.

        Args:
            instance (Institution): The existing Institution instance.
            validated_data (dict): The validated data for the update.

        Returns:
            Institution: The updated Institution instance.
        """
        validated_data.pop("user", None)
        validated_data["updated_at"] = get_timezone()

        return super().update(instance, validated_data)


class UserInstitutionSerializer(ModelSerializer):
    """
    Serializer for the Institution model, for use within User serialization.

    This serializer provides a read-only representation of institutions,
    including their courses, to be nested within the User serializer.
    """

    courses = InstitutionCourseSerializer(many=True, read_only=True)

    class Meta:
        model = Institution
        fields = ["id", "name", "created_at", "updated_at", "courses"]
        read_only_fields = ["id", "name", "created_at", "updated_at", "courses"]
