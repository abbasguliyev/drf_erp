from rest_framework import permissions
from core.utils.permission_utils import PermissionUtil


class ContractPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="contract", view=view)
        return perm_util.add_user_permission_to_list()

class ContractChangePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="contractchange", view=view)
        return perm_util.add_user_permission_to_list()

class InstallmentleriPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="installment", view=view)
        return perm_util.add_user_permission_to_list()

class ContractGiftPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="contractgift", view=view)
        return perm_util.add_user_permission_to_list()

class DemoSalesPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="demosales", view=view)
        return perm_util.add_user_permission_to_list()

class ContractCreditorPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="contractcreditor", view=view)
        return perm_util.add_user_permission_to_list()