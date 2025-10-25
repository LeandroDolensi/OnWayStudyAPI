from django.db import models
from environment import get_timezone


class User(models.Model):
    nickname = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, default=get_timezone)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user"
        managed = True

    def __str__(self):
        return self.nickname
