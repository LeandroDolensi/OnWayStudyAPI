import pytest
from decimal import Decimal, ROUND_HALF_UP, DivisionByZero
from django.utils import timezone
import datetime

from apps.user.models import User
from apps.institution.models import Institution
from apps.course.models import Course
from apps.discipline.models import Discipline
from apps.activity.models import Activity

from apps.discipline.service import DisciplineService


@pytest.fixture
def user():
    return User.objects.create(nickname="testuser", password="testpassword")


@pytest.fixture
def institution(user):
    return Institution.objects.create(name="Test University", user=user)


@pytest.fixture
def course(institution):
    return Course.objects.create(
        name="Test Course", acronym="TC", semesters=1, institution=institution
    )


@pytest.fixture
def discipline(course):
    return Discipline.objects.create(name="Test Discipline", course=course, semester=1)


@pytest.fixture
def delivery_date():
    return timezone.now() + datetime.timedelta(days=30)


def create_activity(discipline, weight, grade, date, expected=None):
    return Activity.objects.create(
        discipline=discipline,
        name=f"Activity (W:{weight}, G:{grade})",
        grade_weight=Decimal(weight) if weight is not None else None,
        grade_result=Decimal(grade) if grade is not None else None,
        expected_grade=Decimal(expected) if expected is not None else None,
        delivery_date=date,
    )


@pytest.mark.django_db
class TestDisciplineService:

    def test_bug_all_activities_completed_and_failed_raises_division_by_zero(
        self, discipline, delivery_date
    ):
        create_activity(discipline, "5.0", "5.0", delivery_date)
        create_activity(discipline, "5.0", "5.0", delivery_date)

        service = DisciplineService(discipline)

        service.update_expected_grades()

    def test_no_activities(self, discipline):
        service = DisciplineService(discipline)
        service.update_expected_grades()
        assert discipline.activities.count() == 0

    def test_total_weight_less_than_10_returns_early(self, discipline, delivery_date):
        act_1 = create_activity(discipline, "5.0", None, delivery_date, "9.99")

        service = DisciplineService(discipline)
        service.update_expected_grades()

        act_1.refresh_from_db()
        assert act_1.expected_grade == Decimal("9.99")

    def test_no_completed_activities_all_pending(self, discipline, delivery_date):
        act_1 = create_activity(discipline, "4.0", None, delivery_date)
        act_2 = create_activity(discipline, "6.0", None, delivery_date)

        service = DisciplineService(discipline)
        service.update_expected_grades()

        act_1.refresh_from_db()
        act_2.refresh_from_db()

        assert act_1.expected_grade == Decimal("6.00")
        assert act_2.expected_grade == Decimal("6.00")

    def test_some_completed_some_pending(self, discipline, delivery_date):
        create_activity(discipline, "3.0", "10.0", delivery_date)
        act_pending = create_activity(discipline, "7.0", None, delivery_date)

        service = DisciplineService(discipline)
        service.update_expected_grades()

        act_pending.refresh_from_db()

        assert act_pending.expected_grade == Decimal("4.29")

    def test_already_passed_expected_grade_is_zero(self, discipline, delivery_date):
        create_activity(discipline, "7.0", "10.0", delivery_date)
        act_pending = create_activity(discipline, "3.0", None, delivery_date)

        service = DisciplineService(discipline)
        service.update_expected_grades()

        act_pending.refresh_from_db()
        assert act_pending.expected_grade == Decimal("0.00")

    def test_impossible_to_pass_clamps_at_max_grade(self, discipline, delivery_date):
        create_activity(discipline, "9.0", "0.0", delivery_date)
        act_pending = create_activity(discipline, "1.0", None, delivery_date)

        service = DisciplineService(discipline)
        service.update_expected_grades()

        act_pending.refresh_from_db()
        assert act_pending.expected_grade == Decimal("10.00")

    def test_all_activities_completed_and_passed(self, discipline, delivery_date):
        act_1 = create_activity(discipline, "5.0", "8.0", delivery_date)  # 40 pts
        act_2 = create_activity(discipline, "5.0", "8.0", delivery_date)  # 40 pts

        service = DisciplineService(discipline)
        service.update_expected_grades()

        act_1.refresh_from_db()
        act_2.refresh_from_db()
        assert act_1.expected_grade is None
        assert act_2.expected_grade is None

    def test_clear_all_expected_grades_logic(self, discipline, delivery_date):
        act_1 = create_activity(discipline, None, None, delivery_date, "5.00")
        act_2 = create_activity(discipline, "1.0", None, delivery_date, "5.00")

        service = DisciplineService(discipline)
        service.update_expected_grades()

        act_1.refresh_from_db()
        act_2.refresh_from_db()

        assert act_1.expected_grade is None
        assert act_2.expected_grade == Decimal("5.00")

    def test_activities_with_none_weight_are_ignored_by_main_logic(
        self, discipline, delivery_date
    ):
        act_1 = create_activity(discipline, "10.0", None, delivery_date)
        act_2 = create_activity(discipline, None, "10.0", delivery_date)

        service = DisciplineService(discipline)
        service.update_expected_grades()

        act_1.refresh_from_db()
        act_2.refresh_from_db()

        assert act_1.expected_grade == Decimal("6.00")
        assert act_2.expected_grade is None
