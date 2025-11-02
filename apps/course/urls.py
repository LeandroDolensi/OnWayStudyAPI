from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.course.views import CourseViewSet

router = DefaultRouter()

router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("", include(router.urls)),
]
