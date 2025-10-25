from django.db import models
from apps.discipline.models import Discipline
from environment import get_timezone


class Activity(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    result = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, related_name="activities"
    )
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "activity"
        managed = True

    def __str__(self):
        return self.name
