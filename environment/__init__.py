import os
from django.utils import timezone


ON_WAY_STUDY_DB_USER = os.getenv("ON_WAY_STUDY_DB_USER")
ON_WAY_STUDY_DB_PASSWORD = os.getenv("ON_WAY_STUDY_DB_PASSWORD")
ON_WAY_STUDY_DJANGO_SECRET_KEY = os.getenv("ON_WAY_STUDY_DJANGO_SECRET_KEY")


def get_timezone():
    return timezone.localtime(timezone.now()).replace(microsecond=0)
