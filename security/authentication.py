import base64
from django.contrib.auth.hashers import check_password
from rest_framework import authentication
from rest_framework import exceptions
from apps.user.models import User
from typing import List
from rest_framework.request import HttpRequest


class OnWayStudyBaseAuthentication(authentication.BaseAuthentication):
    """
    Custom Basic Authentication using `nickname` and `password`.

    Clients must provide an `Authorization` header in the format:
        `Basic <base64_encoded_nickname:password>`

    This authentication backend is designed to work with the custom `User`
    model, authenticating against the `nickname` field instead of
    the standard `username`.
    """

    def authenticate(self, request: HttpRequest):
        """
        Authenticates the request based on `nickname` and `password`.

        This is the main entry point called by DRF. It orchestrates
        the validation, decoding, and user verification process.

        Args:
            request: The HttpRequest object.

        Returns:
            A tuple of (user, None) on successful authentication.
            Returns None if the authentication scheme is not `Basic`.

        Raises:
            exceptions.AuthenticationFailed: If credentials are invalid,
                malformed, or the user/password do not match.
        """
        basic_auth_header = authentication.get_authorization_header(request).split()

        if not self._is_authenticated(basic_auth_header, request):
            return None

        self._validate_auth_header(basic_auth_header)
        nickname, password = self._get_auth_data(basic_auth_header)

        user = self._get_user(nickname)
        self._check_password(password, user)

        return (user, None)

    def _is_authenticated(
        self, basic_auth_header: List[str], request: HttpRequest
    ) -> bool:
        """
        Checks if a user is authenticated using Basic Authentication standards.
        The only exception to this rule is the operation to create a new user.

        Args:
            basic_auth_header (List[str]): The split list from the `Authorization` header
                               (e.g., [b"Basic", b"YWxpY2U6MTIzNA=="]).
            request (HttpRequest): The HttpRequest object

        Raises:
            exceptions.NotAuthenticated: if is not operation to create a new user

        Returns:
            bool: True if has Basic Authentication, otherwise False
        """
        if basic_auth_header and basic_auth_header[0].lower() == b"basic":
            return True

        if not self._is_create_user_method(request):
            raise exceptions.NotAuthenticated(
                """Clients must provide an 'Authorization' header in the format:
                'Basic <base64_encoded_nickname:password>'"""
            )

        return False

    def _is_create_user_method(self, request: HttpRequest) -> bool:
        """Check if the request method and path correspond to the operation of creating a new user.

        Args:
            request (HttpRequest): The HttpRequest object

        Returns:
            bool: True if is the operation to create a new user, otherwise False
        """
        if request.method == "POST" and request.path.endswith("/users/"):
            return True

        return False

    def _validate_auth_header(self, basic_auth_header: List[str]):
        """
        Validates the structure of the `Authorization` header list.

        Checks if the header contains the expected number of parts
        (e.g., just `Basic` or `Basic` with too many spaces).

        Args:
            basic_auth_header: The split list from the `Authorization` header
                               (e.g., [b"Basic", b"YWxpY2U6MTIzNA=="]).

        Raises:
            exceptions.AuthenticationFailed: If the header structure is invalid.
        """
        if len(basic_auth_header) == 1:
            raise exceptions.AuthenticationFailed(
                f"Invalid credentials. No data provided: {basic_auth_header}"
            )

        if len(basic_auth_header) > 2:
            raise exceptions.AuthenticationFailed(
                f"Invalid credentials. The token must not contain spaces: {basic_auth_header}."
            )

    def _get_auth_data(self, basic_auth_header: List[str]) -> List[str]:
        """
        Decodes and extracts credentials from the Base64 token.

        Args:
            basic_auth_header: The split list from the `Authorization` header.

        Returns:
            A list containing the [nickname, password].

        Raises:
            exceptions.AuthenticationFailed: If the token is malformed,
                cannot be decoded, or does not split correctly.
        """
        try:
            return base64.b64decode(basic_auth_header[1]).decode().split(":", 1)
        except (UnicodeDecodeError, ValueError, TypeError) as e:
            raise exceptions.AuthenticationFailed(
                f"Invalid credentials. Could not decode: {e}"
            )

    def _get_user(self, nickname: str) -> User:
        """
        Retrieves the user from the database by their nickname.

        Args:
            nickname: The nickname provided in the credentials.

        Returns:
            The User instance if found.

        Raises:
            exceptions.AuthenticationFailed: If the user does not exist.
        """
        try:
            return User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(f"User '{nickname}' not found.")

    def _check_password(self, password: str, user: User):
        """
        Validates the provided password against the user's stored hash.

        Args:
            password: The plain-text password from the credentials.
            user: The User instance retrieved from the database.

        Raises:
            exceptions.AuthenticationFailed: If the password is incorrect.
        """
        if not check_password(password, user.password):
            raise exceptions.AuthenticationFailed("Incorrect password.")
