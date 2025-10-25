from django.db import models
from apps.institution.models import Institution
from environment import get_timezone


class Course(models.Model):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=10)
    semesters = models.PositiveIntegerField()
    instituition = models.ForeignKey(
        Institution, on_delete=models.CASCADE, related_name="courses"
    )
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "course"
        managed = True

    def __str__(self):
        return f"{self.name} ({self.acronym})"
