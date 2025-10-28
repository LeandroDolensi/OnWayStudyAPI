from rest_framework.serializers import ModelSerializer
from apps.institution.models import Institution
from rest_framework.exceptions import NotAuthenticated, ValidationError
from django.db import IntegrityError
from environment import get_timezone
from apps.user.models import User


class InstitutionSerializer(ModelSerializer):
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
        validated_data["user"] = self._get_user()

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(
                f"The Institution name {validated_data.get("name", "")} alread exist."
            )

    def update(self, instance, validated_data):
        validated_data.pop("user", None)
        validated_data["updated_at"] = get_timezone()

        return super().update(instance, validated_data)

    def _get_user(self) -> User:
        """
        It retrieves the user responsible for the request.
        If the request is not found or the request does not have an associated user, an exception is raised.

        Raises:
            NotAuthenticated: request not found or the request does not have an associated user.

        Returns:
            User: user responsible for the request
        """
        request = self.context.get("request")

        if not request or not hasattr(request, "user"):
            raise NotAuthenticated("Invalid request. No user assigned to the request.")

        return request.user
