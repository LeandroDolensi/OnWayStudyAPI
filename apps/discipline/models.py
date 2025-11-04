from django.db import models
from apps.course.models import Course
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class Discipline(models.Model, PermissionBaseModel):
    class FinalStatusChoices(models.TextChoices):
        FAILED = "FAILED", "Failed"
        RECOVERY = "RECOVERY", "Recovery"
        APPROVED = "APPROVED", "Approved"

    name = models.CharField(max_length=200)
    extra_information = models.TextField(blank=True, null=True)
    final_grade = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    final_result = models.CharField(
        max_length=20, choices=FinalStatusChoices.choices, blank=True, null=True
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="disciplines"
    )
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    linked_to = "course"

    class Meta:
        db_table = "discipline"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["name", "course"], name="unique_discipline_name"
            )
        ]

    def __str__(self):
        return f"{self.course.acronym}: {self.name}"
