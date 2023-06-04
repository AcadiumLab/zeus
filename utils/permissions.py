from rest_framework.permissions import *


class IsVerified(BasePermission):
    """
    Allows access only to verified users.
    """
    message = 'Email is not verified'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_verified)
