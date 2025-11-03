from django.db import models
from apps.user.models import User
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class Institution(models.Model, PermissionBaseModel):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="institutions"
    )
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    linked_to = "user"

    class Meta:
        db_table = "institution"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"], name="unique_institution_name"
            )
        ]

    def __str__(self):
        return self.name
