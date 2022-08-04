from rest_framework import permissions
from restAPI.v1.utils.permission_utils import PermissionUtil

class MehsullarPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="mehsullar", view=view)
        return perm_util.add_user_permission_to_list()