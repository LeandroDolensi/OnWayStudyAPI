from django.db import models
from apps.course.models import Course
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class Discipline(models.Model, PermissionBaseModel):
    """
    Represents an academic discipline within a course.

    A discipline has a name, semester, status, and is associated with a course.
    It can also have a final grade and result.

    Attributes:
        name (str): The name of the discipline.
        extra_information (str): Additional information about the discipline.
        semester (int): The semester in which the discipline is taught.
        status (str): The current status of the discipline (e.g., 'In Progress', 'Completed').
        final_grade (Decimal): The final grade in the discipline.
        final_result (str): The final result (e.g., 'Approved', 'Failed').
        course (Course): The course to which the discipline belongs.
        created_at (datetime): The timestamp when the discipline was created.
        updated_at (datetime): The timestamp when the discipline was last updated.
    """

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
        """
        Returns a string representation of the discipline.

        Returns:
            str: A string in the format "Course Acronym: Discipline Name".
        """
        return f"{self.course.acronym}: {self.name}"


class PrerequisiteDiscipline(models.Model):
    """
    Represents the prerequisite relationship between two disciplines.

    This model defines a directional link where one discipline (the main_discipline)
    has another discipline (the prerequisite) as a requirement.

    Attributes:
        main_discipline (Discipline): The discipline that has a prerequisite.
        prerequisite (Discipline): The discipline that is a prerequisite.
        created_at (datetime): The timestamp when the relationship was created.
        updated_at (datetime): The timestamp when the relationship was last updated.
    """

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
        """
        Returns a string representation of the prerequisite relationship.

        Returns:
            str: A string in the format "Prerequisite Name -> Main Discipline Name".
        """
        return f"{self.prerequisite.name} -> {self.main_discipline.name}"
