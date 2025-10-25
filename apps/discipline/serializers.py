from rest_framework.serializers import ModelSerializer
from apps.discipline.models import Discipline


class DisciplineSerializer(ModelSerializer):

    class Meta:
        model = Discipline
        fields = "__all__"
