from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allow access only to admin or super admin users."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "is_admin", False))


class IsSuperAdmin(BasePermission):
    """Allow access only to super admin users."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "is_super_admin", False))

