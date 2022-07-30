from rest_framework import permissions
from restAPI.utils.permission_utils import PermissionUtil

class OfisKassaPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="ofiskassa", view=view)
        return perm_util.add_user_permission_to_list()

class ShirketKassaPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shirketkassa", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingKassaPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingkassa", view=view)
        return perm_util.add_user_permission_to_list()

class PulAxiniPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="pulaxini", view=view)
        return perm_util.add_user_permission_to_list()