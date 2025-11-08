import pytest
import base64
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from faker import Faker
from apps.user.models import User
from environment import ON_WAY_STUDY_API_KEY_SIGNARURE
from django.contrib.auth.hashers import make_password

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
