from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.discipline.views import DisciplineViewSet

router = DefaultRouter()

router.register(r"disciplines", DisciplineViewSet, basename="disciplines")

urlpatterns = [
    path("", include(router.urls)),
]
