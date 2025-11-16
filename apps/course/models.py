from django.db import models
from apps.institution.models import Institution
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class Course(models.Model, PermissionBaseModel):
    """
    Represents an academic course within an institution.

    A course has a name, an acronym, a number of semesters, and is associated
    with an institution.

    Attributes:
        name (str): The name of the course.
        acronym (str): The acronym for the course.
        semesters (int): The total number of semesters in the course.
        institution (Institution): The institution to which the course belongs.
        created_at (datetime): The timestamp when the course was created.
        updated_at (datetime): The timestamp when the course was last updated.
    """

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
        """
        Returns a string representation of the course.

        Returns:
            str: A string in the format "Course Name (ACRONYM)".
        """
        return f"{self.name} ({self.acronym})"
