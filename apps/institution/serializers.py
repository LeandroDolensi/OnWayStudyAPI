from apps.institution.models import Institution
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django_libs.custom_serializer import CustomModelSerializer
from environment import get_timezone


class InstitutionSerializer(CustomModelSerializer):
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
