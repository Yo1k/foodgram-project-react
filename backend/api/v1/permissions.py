from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Sets permission to create new object only for authorized user,
    however any user can view object(s).

    Permission allowing only an author of an object
    or an admin to edit it.
    Assumes the model instance has an `author` attribute.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user == obj.author
            or request.user.is_staff
        )
