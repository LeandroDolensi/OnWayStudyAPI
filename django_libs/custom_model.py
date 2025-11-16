class PermissionBaseModel:
    """
    A base model for handling object-level permissions.

    This model provides a `linked_to` attribute that specifies the name of the
    related field that links to the owner of the object. This is used by the
    `IsOwner` permission class to determine ownership.
    """

    linked_to: str = "user"
