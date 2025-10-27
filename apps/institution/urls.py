from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.institution.views import InstitutionViewSet

router = DefaultRouter()

router.register(r"institutions", InstitutionViewSet, basename="institution")

urlpatterns = [
    path("", include(router.urls)),
]
