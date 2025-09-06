from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    """
    Base class for role-based permissions.
    Subclass this and set allowed_roles = ["ROLE1", "ROLE2"]
    """
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in self.allowed_roles
        )


# ✅ Factory Function (for multiple roles in one line)
def role_permission(roles):
    """
    Dynamically create a RolePermission for given roles.
    Example: permission_classes = [role_permission(["DOCTOR", "NURSE"])]
    """
    class CustomRolePermission(RolePermission):
        allowed_roles = roles
    return CustomRolePermission
