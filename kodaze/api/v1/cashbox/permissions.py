from rest_framework import permissions
from api.v1.utils.permission_utils import PermissionUtil

class OfficeCashboxPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officecashbox", view=view)
        return perm_util.add_user_permission_to_list()

class CompanyCashboxPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="companycashbox", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingCashboxPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingcashbox", view=view)
        return perm_util.add_user_permission_to_list()

class CashFlowPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="cashflow", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingCashboxOperationPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingcashboxoperation", view=view)
        return perm_util.add_user_permission_to_list()

class OfficeCashboxOperationPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officecashboxoperation", view=view)
        return perm_util.add_user_permission_to_list()