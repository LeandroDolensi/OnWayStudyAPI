from rest_framework.serializers import ModelSerializer
from apps.institution.models import Institution


class InstituitionSerializer(ModelSerializer):

    class Meta:
        model = Institution
        fields = "__all__"
