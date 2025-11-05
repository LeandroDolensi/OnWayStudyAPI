from apps.discipline.models import Discipline
from apps.activity.models import Activity
from decimal import Decimal, ROUND_HALF_UP


class DisciplineService:
    _discipline: Discipline

    TARGET_AVERAGE = Decimal("6.0")
    TOTAL_WEIGHT_NEEDED = Decimal("10.0")
    TOTAL_POINTS_NEEDED = Decimal("60.000")
    MAX_GRADE = Decimal("10.0")
    MIN_GRADE = Decimal("0.0")

    def __init__(self, discipline_instance: Discipline):
        self._discipline = discipline_instance

    def update_expected_grades(self):
        activities = self._discipline.activities.all()
        if not activities:
            return

        self._clear_all_expected_grades(activities)

        total_weight = Decimal("0.0")
        total_points_achieved = Decimal("0.0")
        pending_weight = Decimal("0.0")

        pending_activities = []
        completed_activities = []

        for activity in activities:
            if activity.grade_weight is None:
                continue

            weight = activity.grade_weight
            total_weight += weight

            if activity.grade_result is not None:
                total_points_achieved += activity.grade_result * weight
                completed_activities.append(activity)
            else:
                pending_weight += weight
                pending_activities.append(activity)

        if total_weight < self.TOTAL_WEIGHT_NEEDED:
            # só pode calcular a nota esperada se a soma dos pesos forem 10
            return

        points_to_achieve = self.TOTAL_POINTS_NEEDED - total_points_achieved
        expected_grade = self.MIN_GRADE

        if points_to_achieve > self.MIN_GRADE:
            expected_grade = (points_to_achieve / pending_weight).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        expected_grade = max(self.MIN_GRADE, min(expected_grade, self.MAX_GRADE))

        self._update_pending_activities(pending_activities, expected_grade)

        if pending_activities:
            Activity.objects.bulk_update(pending_activities, ["expected_grade"])

    def _update_pending_activities(
        self, pending_activities: list, expected_grade: Decimal
    ):
        for activity in pending_activities:
            activity.expected_grade = expected_grade

    def _clear_all_expected_grades(self, activities: list):
        activities_to_update = []
        for activity in activities:
            if activity.expected_grade is not None and activity.grade_weight is None:
                activity.expected_grade = None
                activities_to_update.append(activity)

        if activities_to_update:
            Activity.objects.bulk_update(activities_to_update, ["expected_grade"])
