from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import NotAuthenticated
from apps.user.models import User


class CustomModelSerializer(ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_user(self) -> User:
        """
        It retrieves the user responsible for the request.
        If the request is not found or the request does not have an associated user, an exception is raised.

        Raises:
            NotAuthenticated: request not found or the request does not have an associated user.

        Returns:
            User: user responsible for the request
        """
        request = self.context.get("request")

        if not request or not hasattr(request, "user"):
            raise NotAuthenticated("Invalid request. No user assigned to the request.")

        return request.user
