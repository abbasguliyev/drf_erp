from rest_framework import permissions
from restAPI.utils.permission_utils import PermissionUtil

class ServisPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="servis", view=view)
        return perm_util.add_user_permission_to_list()

class ServisOdemePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="servisodeme", view=view)
        return perm_util.add_user_permission_to_list()
