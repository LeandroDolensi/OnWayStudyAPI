from django.db import models
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class User(models.Model, PermissionBaseModel):
    """
    Represents a user of the application.

    A user has a unique nickname and a password.

    Attributes:
        nickname (str): The unique nickname of the user.
        password (str): The hashed password of the user.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
    """

    nickname = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user"
        managed = True

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: The nickname of the user.
        """
        return self.nickname
