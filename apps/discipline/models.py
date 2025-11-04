from django.db import models
from apps.course.models import Course
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class Discipline(models.Model, PermissionBaseModel):
    class FinalStatusChoices(models.TextChoices):
        FAILED = "FAILED", "Failed"
        RECOVERY = "RECOVERY", "Recovery"
        APPROVED = "APPROVED", "Approved"

    class DisciplineStatusChoice(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        WAITING = "WAITING", "Waiting"
        AWAITING_PREREQUISITE = "AWAITING_PREREQUISITE", "Awaiting Prerequisite"

    name = models.CharField(max_length=200)
    extra_information = models.TextField(blank=True, null=True)
    semester = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=DisciplineStatusChoice.choices,
        default=DisciplineStatusChoice.WAITING,
    )
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


class PrerequisiteDiscipline(models.Model):
    main_discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, related_name="prerequisites"
    )
    prerequisite = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, related_name="is_prerequisite_for"
    )
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "prerequisite_discipline"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["main_discipline", "prerequisite"],
                name="unique_discipline_prerequisite",
            )
        ]

    def __str__(self):
        return f"{self.prerequisite.name} -> {self.main_discipline.name}"
