from rest_framework import permissions
from core.utils.permission_utils import PermissionUtil

class OperationPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="operation", view=view)
        return perm_util.add_user_permission_to_list()

class StockPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="stok", view=view)
        return perm_util.add_user_permission_to_list()

class WarehouseRequestPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="warehouserequest", view=view)
        return perm_util.add_user_permission_to_list()

class WarehousePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="warehouse", view=view)
        return perm_util.add_user_permission_to_list()
