from rest_framework import permissions
from api.v1.utils.permission_utils import PermissionUtil

class TransferFromOfficeToCompanyPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="transferfromofficetocompany", view=view)
        return perm_util.add_user_permission_to_list()

class TransferFromCompanyToOfficesPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="transferfromcompanytooffices", view=view)
        return perm_util.add_user_permission_to_list()

class TransferFromCompanyToHoldingPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="transferfromcompanytoholding", view=view)
        return perm_util.add_user_permission_to_list()

class TransferFromHoldingToCompanyPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="transferfromholdingtocompany", view=view)
        return perm_util.add_user_permission_to_list()