from rest_framework import permissions
from core.utils.permission_utils import PermissionUtil

class HoldingTransferPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingtransfer", view=view)
        return perm_util.add_user_permission_to_list()

class CompanyTransferPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="companytransfer", view=view)
        return perm_util.add_user_permission_to_list()

class OfficeTransferPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officetransfer", view=view)
        return perm_util.add_user_permission_to_list()