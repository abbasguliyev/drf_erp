from rest_framework import permissions
from core.utils.permission_utils import PermissionUtil


class UserPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="user", view=view)
        return perm_util.add_user_permission_to_list()

class EmployeeStatusPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="employeestatus", view=view)
        return perm_util.add_user_permission_to_list()

class RegionPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="region", view=view)
        return perm_util.add_user_permission_to_list()

class CustomerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="customer", view=view)
        return perm_util.add_user_permission_to_list()

class PermissionModelPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="permission", view=view)
        return perm_util.add_user_permission_to_list()

class GroupPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="group", view=view)
        return perm_util.add_user_permission_to_list()

class PasswordResetPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="passwordreset", view=view)
        return perm_util.add_user_permission_to_list()

class EmployeeActivityPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="employeeactivity", view=view)
        return perm_util.add_user_permission_to_list()