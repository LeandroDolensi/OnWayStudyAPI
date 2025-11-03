from django.db import models
from apps.course.models import Course
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class Discipline(models.Model, PermissionBaseModel):
    name = models.CharField(max_length=200)
    extra_information = models.TextField(blank=True, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="disciplines"
    )
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    linked_to = "course"

    class Meta:
        db_table = "discipline"
        managed = True

    def __str__(self):
        return self.name
