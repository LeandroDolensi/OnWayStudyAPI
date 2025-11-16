from django.db import models
from apps.discipline.models import Discipline
from django_libs.custom_model import PermissionBaseModel
from environment import get_timezone


class Activity(models.Model, PermissionBaseModel):
    """
    Represents an academic activity within a discipline.

    An activity is a task or assignment that has a name, status, and due date.
    It can also have a grade weight, an expected grade, and a final grade.

    Attributes:
        name (str): The name of the activity.
        status (str): The current status of the activity (e.g., 'Pending', 'In Progress').
        grade_weight (Decimal): The weight of the activity's grade in the discipline.
        expected_grade (Decimal): The grade the user expects to get.
        grade_result (Decimal): The actual grade received for the activity.
        delivery_date (datetime): The due date for the activity.
        discipline (Discipline): The discipline to which the activity belongs.
        created_at (datetime): The timestamp when the activity was created.
        updated_at (datetime): The timestamp when the activity was last updated.
    """

    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    grade_weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    expected_grade = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    grade_result = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    delivery_date = models.DateTimeField()
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, related_name="activities"
    )
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    linked_to = "discipline"

    class Meta:
        db_table = "activity"
        managed = True

    def __str__(self):
        """
        Returns a string representation of the activity.

        Returns:
            str: A string in the format "Discipline Name: Activity Name".
        """
        return f"{self.discipline.name}: {self.name}"
