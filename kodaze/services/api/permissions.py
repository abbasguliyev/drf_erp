from rest_framework import permissions
from core.utils.permission_utils import PermissionUtil

class ServicePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="service", view=view)
        return perm_util.add_user_permission_to_list()

class ServicePaymentPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="servicepayment", view=view)
        return perm_util.add_user_permission_to_list()
