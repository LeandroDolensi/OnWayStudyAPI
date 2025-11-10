import pytest
import base64
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from faker import Faker
from apps.user.models import User
from environment import ON_WAY_STUDY_API_KEY_SIGNARURE
from django.contrib.auth.hashers import make_password, check_password
from apps.institution.models import Institution
from apps.course.models import Course
from apps.discipline.models import Discipline


fake = Faker()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_headers():
    return {
        "HTTP_X_APP_SIGNATURE": ON_WAY_STUDY_API_KEY_SIGNARURE,
    }


@pytest.fixture
def user_data():
    return {
        "nickname": fake.user_name(),
        "password": fake.password(length=12),
    }


@pytest.fixture
def created_user(user_data):
    user = User.objects.create(
        nickname=user_data["nickname"], password=make_password(user_data["password"])
    )
    return user, user_data["password"]


@pytest.fixture
def authenticated_client(api_client, created_user, common_headers):
    user, plain_password = created_user

    creds = f"{user.nickname}:{plain_password}"
    creds_b64 = base64.b64encode(creds.encode("utf-8")).decode("utf-8")

    client = api_client
    client.credentials(HTTP_AUTHORIZATION=f"Basic {creds_b64}")

    client.defaults.update(common_headers)

    return client, user


@pytest.fixture
def authenticated_client_b(api_client, common_headers, user_data):
    hashed_password_b = make_password(user_data["password"])
    user_b = User.objects.create(nickname=fake.user_name(), password=hashed_password_b)

    creds_b = f"{user_b.nickname}:{user_data['password']}"
    creds_b64 = base64.b64encode(creds_b.encode("utf-8")).decode("utf-8")

    client_b = APIClient()
    client_b.credentials(HTTP_AUTHORIZATION=f"Basic {creds_b64}")
    client_b.defaults.update(common_headers)

    return client_b, user_b


@pytest.fixture
def institution_a(created_user):
    user, _ = created_user
    return Institution.objects.create(name=fake.company(), user=user)


@pytest.fixture
def institution_b(authenticated_client_b):
    _, user_b = authenticated_client_b
    return Institution.objects.create(name=fake.company(), user=user_b)


@pytest.fixture
def course_a(institution_a):
    return Course.objects.create(
        name="Engenharia de Software",
        acronym="ES",
        semesters=10,
        institution=institution_a,
    )


@pytest.fixture
def course_b(institution_b):
    return Course.objects.create(
        name="Medicina", acronym="MED", semesters=12, institution=institution_b
    )


@pytest.mark.django_db
class TestUserAPI:
    def test_create_user_success(self, api_client, common_headers, user_data):
        url = reverse("user-list")
        response = api_client.post(url, data=user_data, headers=common_headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert User.objects.first().nickname == user_data["nickname"]

        assert User.objects.first().password != user_data["password"]
        assert "password" not in response.data

    def test_create_user_duplicate_nickname_fails(
        self, api_client, common_headers, created_user
    ):

        user, _ = created_user
        url = reverse("user-list")
        data = {
            "nickname": user.nickname,
            "password": "anotherpassword123",
        }

        response = api_client.post(url, data=data, headers=common_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "nickname" in response.data
        assert "suggestions" in response.data
        assert len(response.data["suggestions"]) > 0

    def test_create_user_empty_nickname_fails(self, api_client, common_headers):
        url = reverse("user-list")
        data = {"nickname": "", "password": "password123"}
        response = api_client.post(url, data=data, headers=common_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "nickname" in response.data

    def test_create_user_empty_password_fails(self, api_client, common_headers):
        url = reverse("user-list")
        data = {"nickname": "testuser", "password": ""}
        response = api_client.post(url, data=data, headers=common_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

    def test_list_user_returns_self(self, authenticated_client):
        client, user = authenticated_client
        url = reverse("user-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == user.id
        assert response.data[0]["nickname"] == user.nickname

    def test_list_user_unauthenticated_fails(self, api_client, common_headers):
        url = reverse("user-list")
        response = api_client.get(url, headers=common_headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_self_success(self, authenticated_client):
        client, user = authenticated_client
        url = reverse("user-detail", kwargs={"id": user.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user.id
        assert "institutions" in response.data
        assert response.data["institutions"] == []

    def test_retrieve_other_user_fails(self, authenticated_client, user_data):
        client, user_a = authenticated_client

        user_b = User.objects.create(
            nickname=fake.user_name(), password=make_password(user_data["password"])
        )

        url = reverse("user-detail", kwargs={"id": user_b.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_self_success(self, authenticated_client):
        client, user = authenticated_client
        url = reverse("user-detail", kwargs={"id": user.id})

        new_nickname = "novo_nickname_123"
        data = {"nickname": new_nickname, "password": "password123"}

        response = client.put(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["nickname"] == new_nickname

        user.refresh_from_db()
        assert user.nickname == new_nickname

    def test_delete_self_success(self, authenticated_client):
        client, user = authenticated_client
        url = reverse("user-detail", kwargs={"id": user.id})

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.filter(id=user.id).exists() is False

    def test_delete_other_user_fails(self, authenticated_client, user_data):
        client, user_a = authenticated_client
        user_b = User.objects.create(
            nickname=fake.user_name(), password=make_password(user_data["password"])
        )

        url = reverse("user-detail", kwargs={"id": user_b.id})
        response = client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert User.objects.filter(id=user_b.id).exists() is True


@pytest.mark.django_db
class TestInstitutionAPI:
    def test_create_institution_unauthenticated_fails(self, api_client, common_headers):
        url = reverse("institution-list")
        data = {"name": "Minha Universidade"}
        response = api_client.post(url, data=data, headers=common_headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_institution_authenticated_success(self, authenticated_client):
        client, user = authenticated_client
        url = reverse("institution-list")
        data = {"name": "Minha Universidade"}

        response = client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Institution.objects.count() == 1

        institution = Institution.objects.first()
        assert institution.name == "Minha Universidade"
        assert institution.user == user  # Verifica se o 'owner' está correto

    def test_create_duplicate_institution_name_same_user_fails(
        self, authenticated_client
    ):
        client, user = authenticated_client
        url = reverse("institution-list")
        data = {"name": "Universidade Repetida"}

        response_1 = client.post(url, data=data)
        assert response_1.status_code == status.HTTP_201_CREATED

        response_2 = client.post(url, data=data)

        assert response_2.status_code == status.HTTP_400_BAD_REQUEST
        assert "alread exist" in str(response_2.data)

    def test_create_duplicate_institution_name_different_user_succeeds(
        self, authenticated_client, authenticated_client_b
    ):
        client_a, user_a = authenticated_client
        client_b, user_b = authenticated_client_b

        url = reverse("institution-list")
        data = {"name": "Universidade Comum"}

        response_a = client_a.post(url, data=data)
        assert response_a.status_code == status.HTTP_201_CREATED

        response_b = client_b.post(url, data=data)
        assert response_b.status_code == status.HTTP_201_CREATED

        assert Institution.objects.count() == 2
        assert (
            Institution.objects.filter(user=user_a).first().name == "Universidade Comum"
        )
        assert (
            Institution.objects.filter(user=user_b).first().name == "Universidade Comum"
        )

    def test_list_institutions_returns_only_own(
        self, authenticated_client, authenticated_client_b
    ):
        client_a, user_a = authenticated_client
        client_b, user_b = authenticated_client_b

        Institution.objects.create(name="Uni A1", user=user_a)
        Institution.objects.create(name="Uni A2", user=user_a)

        Institution.objects.create(name="Uni B1", user=user_b)

        assert Institution.objects.count() == 3

        url = reverse("institution-list")
        response_a = client_a.get(url)

        assert response_a.status_code == status.HTTP_200_OK
        assert len(response_a.data) == 2
        assert response_a.data[0]["name"] == "Uni A1"
        assert response_a.data[1]["name"] == "Uni A2"

    def test_retrieve_other_user_institution_fails(
        self, authenticated_client, authenticated_client_b
    ):
        client_a, user_a = authenticated_client
        client_b, user_b = authenticated_client_b

        inst_b = Institution.objects.create(name="Instituição de B", user=user_b)

        url = reverse("institution-detail", kwargs={"id": inst_b.id})
        response_a = client_a.get(url)

        assert response_a.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCourseAPI:
    def test_create_course_unauthenticated_fails(
        self, api_client, common_headers, institution_a
    ):
        url = reverse("courses-list")
        data = {
            "name": "Engenharia de Software",
            "acronym": "ES",
            "semesters": 10,
            "institution": institution_a.id,
        }
        response = api_client.post(url, data=data, headers=common_headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_course_success(self, authenticated_client, institution_a):

        client, user = authenticated_client
        url = reverse("courses-list")

        data = {
            "name": "Engenharia de Software",
            "acronym": "ES",
            "semesters": 10,
            "institution": institution_a.id,
        }

        response = client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.count() == 1
        course = Course.objects.first()
        assert course.name == "Engenharia de Software"
        assert course.institution == institution_a

    def test_create_course_for_other_user_institution_fails(
        self, authenticated_client, institution_b
    ):
        client, user_a = authenticated_client
        url = reverse("courses-list")

        data = {
            "name": "Curso Malicioso",
            "acronym": "MAL",
            "semesters": 1,
            "institution": institution_b.id,
        }

        response = client.post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "institution" in response.data
        assert "does not exist" in str(response.data["institution"][0])
        assert Course.objects.count() == 0

    def test_list_courses_returns_only_own(
        self, authenticated_client, authenticated_client_b, institution_a, institution_b
    ):
        client_a, user_a = authenticated_client

        Course.objects.create(
            name="Curso A1", acronym="A1", semesters=1, institution=institution_a
        )
        Course.objects.create(
            name="Curso A2", acronym="A2", semesters=1, institution=institution_a
        )

        Course.objects.create(
            name="Curso B1", acronym="B1", semesters=1, institution=institution_b
        )

        assert Course.objects.count() == 3

        url = reverse("courses-list")
        response_a = client_a.get(url)

        assert response_a.status_code == status.HTTP_200_OK
        assert len(response_a.data) == 2
        assert response_a.data[0]["name"] == "Curso A1"
        assert response_a.data[1]["name"] == "Curso A2"

    def test_retrieve_other_user_course_fails(
        self, authenticated_client, institution_b
    ):
        client_a, user_a = authenticated_client

        course_b = Course.objects.create(
            name="Curso B1", acronym="B1", semesters=1, institution=institution_b
        )

        url = reverse("courses-detail", kwargs={"id": course_b.id})
        response_a = client_a.get(url)

        assert response_a.status_code == status.HTTP_404_NOT_FOUND

    def test_create_duplicate_course_name_same_institution_fails(
        self, authenticated_client, institution_a
    ):
        client, user = authenticated_client
        url = reverse("courses-list")

        data = {
            "name": "Curso Duplicado",
            "acronym": "CD",
            "semesters": 2,
            "institution": institution_a.id,
        }

        response_1 = client.post(url, data=data)
        assert response_1.status_code == status.HTTP_201_CREATED

        response_2 = client.post(url, data=data)

        assert response_2.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response_2.data
        assert "code='unique'" in str(response_2.data)
        assert Course.objects.count() == 1


@pytest.mark.django_db
class TestDisciplineAPI:

    def test_create_discipline_unauthenticated_fails(
        self, api_client, common_headers, course_a
    ):
        url = reverse("disciplines-list")
        data = {
            "name": "Cálculo 1",
            "semester": 1,
            "course": course_a.id,
        }
        response = api_client.post(url, data=data, headers=common_headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_discipline_success(self, authenticated_client, course_a):
        client, user = authenticated_client
        url = reverse("disciplines-list")

        data = {
            "name": "Cálculo 1",
            "semester": 1,
            "course": course_a.id,
        }

        response = client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Discipline.objects.count() == 1
        discipline = Discipline.objects.first()
        assert discipline.name == "Cálculo 1"
        assert discipline.course == course_a

    def test_create_discipline_for_other_user_course_fails(
        self, authenticated_client, course_b
    ):
        client, user_a = authenticated_client
        url = reverse("disciplines-list")

        data = {
            "name": "Disciplina Maliciosa",
            "semester": 1,
            "course": course_b.id,
        }

        response = client.post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "course" in response.data
        assert "does not exist" in str(response.data["course"][0])
        assert Discipline.objects.count() == 0  # Nenhuma disciplina foi criada

    def test_list_disciplines_returns_only_own(
        self, authenticated_client, course_a, course_b
    ):
        client_a, user_a = authenticated_client

        Discipline.objects.create(name="Disciplina A1", semester=1, course=course_a)
        Discipline.objects.create(name="Disciplina A2", semester=2, course=course_a)

        Discipline.objects.create(name="Disciplina B1", semester=1, course=course_b)

        assert Discipline.objects.count() == 3

        url = reverse("disciplines-list")
        response_a = client_a.get(url)

        assert response_a.status_code == status.HTTP_200_OK
        assert len(response_a.data) == 2
        assert response_a.data[0]["name"] == "Disciplina A1"
        assert response_a.data[1]["name"] == "Disciplina A2"

    def test_retrieve_other_user_discipline_fails(self, authenticated_client, course_b):
        client_a, user_a = authenticated_client

        discipline_b = Discipline.objects.create(
            name="Disciplina B1", semester=1, course=course_b
        )

        url = reverse("disciplines-detail", kwargs={"id": discipline_b.id})
        response_a = client_a.get(url)

        assert response_a.status_code == status.HTTP_404_NOT_FOUND

    def test_create_duplicate_discipline_name_same_course_fails(
        self, authenticated_client, course_a
    ):
        client, user = authenticated_client
        url = reverse("disciplines-list")

        data = {
            "name": "Disciplina Duplicada",
            "semester": 3,
            "course": course_a.id,
        }

        response_1 = client.post(url, data=data)
        assert response_1.status_code == status.HTTP_201_CREATED

        response_2 = client.post(url, data=data)

        assert response_2.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response_2.data
        assert "code='unique'" in str(response_2.data)
        assert Discipline.objects.count() == 1
