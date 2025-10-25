import random
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from typing import List, Dict


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "nickname", "created_at", "updated_at", "password"]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "nickname": {
                "validators": [],
            },
        }

    def create(self, validated_data):
        self._validate_nickname(validated_data)
        self._validate_password(validated_data)

        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data.get("password"))

        return super().update(instance, validated_data)

    def _validate_password(self, validated_data: Dict[str, str]):
        """
        Validates and hashes the password.

        Checks if the 'password' field has been provided. If so,
        replaces the value in 'validated_data' with its
        hashed version.

        Args:
            validated_data: The dictionary of validated data from the serializer.

        Raises:
            serializers.ValidationError: If the password is empty or null.
        """
        if not validated_data.get("password", None):
            raise serializers.ValidationError(
                {"password": "The field 'password' cannot be empty."}
            )

        validated_data["password"] = make_password(validated_data.get("password"))

    def _validate_nickname(self, validated_data: Dict[str, str]):
        """
        Validates if the nickname already exists and offers suggestions.

        If the nickname is already in use, it calls the
        _build_nicknames_suggestions method to generate alternatives
        and raises a validation exception with these suggestions.

        Args:
            validated_data: The dictionary of validated data from the serializer.

        Raises:
            serializers.ValidationError: If the nickname already exists.
        """
        nickname = validated_data.get("nickname")

        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError(
                {
                    "nickname": "This nickname already exists. Try one of these:",
                    "suggestions": self._build_nicknames_suggestions(nickname),
                }
            )

    def _build_nicknames_suggestions(self, nickname: str) -> List[str]:
        """
        Generates a list of unique nicknames as suggestions.

        It searches for nicknames by concatenating the original name with a random
        numeric suffix and checks if the generated suggestion already
        exists in the database before adding it to the list.

        Args:
            nickname: The original nickname that already exists.

        Returns:
            A list of up to 5 strings with suggested unique nicknames.
        """
        generated_suggestions = set()
        attempts = 0

        while len(generated_suggestions) < 5 and attempts < 100:
            random_suffix = random.randint(100, 999)
            new_nickname = f"{nickname}{random_suffix}"

            if (
                new_nickname not in generated_suggestions
                and not User.objects.filter(nickname=new_nickname).exists()
            ):
                generated_suggestions.add(new_nickname)

            attempts += 1

        return list(generated_suggestions)
