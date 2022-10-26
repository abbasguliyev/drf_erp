from rest_framework import permissions
from api.v1.utils.permission_utils import PermissionUtil

class AdvancePaymentPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="advancepayment", view=view)
        return perm_util.add_user_permission_to_list()

class SalaryDeductionPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="salarydeduction", view=view)
        return perm_util.add_user_permission_to_list()

class SalaryPunishmentPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="salarypunishment", view=view)
        return perm_util.add_user_permission_to_list()


class BonusPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="bonus", view=view)
        return perm_util.add_user_permission_to_list()

class SalaryViewPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="salaryview", view=view)
        return perm_util.add_user_permission_to_list()

class PaySalaryPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="paysalary", view=view)
        return perm_util.add_user_permission_to_list()

class MonthRangePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="monthrange", view=view)
        return perm_util.add_user_permission_to_list()

class SaleRangePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="salerange", view=view)
        return perm_util.add_user_permission_to_list()

class CommissionInstallmentPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="commissioninstallment", view=view)
        return perm_util.add_user_permission_to_list()

class CommissionSaleRangePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="commissionsalerange", view=view)
        return perm_util.add_user_permission_to_list()

class CommissionPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="commission", view=view)
        return perm_util.add_user_permission_to_list()