from rest_framework import permissions

from django_libs.custom_model import PermissionBaseModel


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
        obj = self.get_obj_user(obj)
        return obj == request.user

    def get_obj_user(self, obj: PermissionBaseModel):
        if hasattr(obj, obj.linked_to):
            obj = self.get_obj_user(getattr(obj, obj.linked_to))

        return obj
