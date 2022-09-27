from rest_framework import permissions
from restAPI.v1.utils.permission_utils import PermissionUtil

class HoldingCashboxIncomePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingcashboxincome", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingCashboxExpensePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingcashboxexpense", view=view)
        return perm_util.add_user_permission_to_list()

class CompanyCashboxIncomePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="companycashboxincome", view=view)
        return perm_util.add_user_permission_to_list()

class CompanyCashboxExpensePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="companycashboxexpense", view=view)
        return perm_util.add_user_permission_to_list()

class OfficeCashboxIncomePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officecashboxincome", view=view)
        return perm_util.add_user_permission_to_list()

class OfficeCashboxExpensePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officecashboxexpense", view=view)
        return perm_util.add_user_permission_to_list()
