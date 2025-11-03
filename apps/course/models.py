from django.db import models
from apps.institution.models import Institution
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class Course(models.Model, PermissionBaseModel):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=10)
    semesters = models.PositiveIntegerField()
    institution = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="courses"
    )
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    linked_to = "institution"

    class Meta:
        db_table = "course"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["name", "institution"],
                name="unique_course_name",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.acronym})"
