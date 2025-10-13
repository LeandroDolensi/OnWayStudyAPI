from django.db import models
from apps.course.models import Course


class Discipline(models.Model):
    name = models.CharField(max_length=200)
    extra_information = models.TextField(blank=True, null=True)
    curso = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="disciplines"
    )

    class Meta:
        db_table = "discipline"
        managed = True

    def __str__(self):
        return self.name
