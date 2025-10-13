from django.db import models
from apps.user.models import User


class Institution(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="institutions"
    )

    def __str__(self):
        return self.name
