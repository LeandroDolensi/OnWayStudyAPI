from django.db import models


class User(models.Model):
    nickname = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = "user"
        managed = True

    def __str__(self):
        return self.nickname
