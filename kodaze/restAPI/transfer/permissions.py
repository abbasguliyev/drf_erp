from rest_framework import permissions
from restAPI.utils.permission_utils import PermissionUtil

class OfisdenShirketeTransferPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="ofisdenshirketetransfer", view=view)
        return perm_util.add_user_permission_to_list()

class ShirketdenOfislereTransferPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shirketdenofisleretransfer", view=view)
        return perm_util.add_user_permission_to_list()

class ShirketdenHoldingeTransferPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shirketdenholdingetransfer", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingdenShirketlereTransferPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingdenshirketleretransfer", view=view)
        return perm_util.add_user_permission_to_list()