from rest_framework.serializers import SlugRelatedField, ModelSerializer
from apps.activity.models import Activity
from apps.discipline.models import Discipline
from django_libs.custom_serializer import CustomModelSerializer


class ActivitySerializer(CustomModelSerializer):
    discipline = SlugRelatedField(slug_field="id", queryset=Discipline.objects.all())

    class Meta:
        model = Activity
        fields = [
            "id",
            "name",
            "status",
            "grade_weight",
            "expected_grade",
            "grade_result",
            "delivery_date",
            "discipline",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["discipline"].queryset = Discipline.objects.filter(
            course__institution__user=self._get_user()
        )

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def _calculate_expected_grade(self, validated_data):
        pass


class DisciplineActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "id",
            "name",
            "status",
            "grade_weight",
            "expected_grade",
            "grade_result",
            "delivery_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
