from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object to edit or view it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Allows access if the logged-in user is the same as the object they are trying to access.

        Args:
            request: `request.user` is the user who was authenticated by **OnWayStudyBaseAuthentication** class.
            obj: `obj` is the instance of the User being accessed.

        Returns:
            _type_: True if the user owns the object. False otherwise.
        """
        return obj == request.user
