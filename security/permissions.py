from rest_framework import permissions

from django_libs.custom_model import PermissionBaseModel


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object to edit or view it.

    This permission class works by recursively traversing the `linked_to`
    attribute of the object until it finds the ultimate user owner.
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
        """
        Recursively traverses the object's relationships to find the ultimate user owner.

        This method follows the `linked_to` attribute on each object to navigate
        through the chain of ownership until it reaches the final user object.

        Args:
            obj (PermissionBaseModel): The object to start the traversal from.

        Returns:
            User: The user object that owns the chain of objects.
        """
        if hasattr(obj, obj.linked_to):
            obj = self.get_obj_user(getattr(obj, obj.linked_to))

        return obj
