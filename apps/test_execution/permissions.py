from rest_framework.permissions import BasePermission


class IsTestRunner(BasePermission):
    """Allow users to manage their own test runs or admins."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_admin", False):
            return True
        return obj.initiated_by_id == getattr(user, "id", None)

