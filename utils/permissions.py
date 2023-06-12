from rest_framework.permissions import *


class IsVerified(BasePermission):
    """
    Allows access only to verified users.
    """
    message = 'Email is not verified'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_verified)


class IsMainUserOrReadOnly(BasePermission):
    """
    Allows access only to main users.
    """
    message = 'You do not have permission to do this action'

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_main
        )
