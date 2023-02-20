from rest_framework import permissions
from core.utils.permission_utils import PermissionUtil

class HoldingPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holding", view=view)
        return perm_util.add_user_permission_to_list()

class DepartmentPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="department", view=view)
        return perm_util.add_user_permission_to_list()


class CompanyPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="company", view=view)
        return perm_util.add_user_permission_to_list()

class OfficePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="office", view=view)
        return perm_util.add_user_permission_to_list()

    def has_object_permission(self, request, view, obj):
        is_admin = super().has_permission(request, view)
        request_user_company = request.user.company
        object_company = obj.company

        return request_user_company == object_company or is_admin

class SectionPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="section", view=view)
        return perm_util.add_user_permission_to_list()

class PositionPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="position", view=view)
        return perm_util.add_user_permission_to_list()

class TeamPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="team", view=view)
        return perm_util.add_user_permission_to_list()

# ******************** Positionye gore permission *****************************************
class PermissionForPositionPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="permissionforposition", view=view)
        return perm_util.add_user_permission_to_list()

# ******************** AppLogo permission *****************************************
class AppLogoPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view=None):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="applogo", view=view)
        return perm_util.add_user_permission_to_list()
