from rest_framework import permissions
from restAPI.utils.permission_utils import PermissionUtil

class EmeliyyatPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="emeliyyat", view=view)
        return perm_util.add_user_permission_to_list()

class StokPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="stok", view=view)
        return perm_util.add_user_permission_to_list()

class AnbarQeydlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="anbarqeydler", view=view)
        return perm_util.add_user_permission_to_list()

class AnbarPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="anbar", view=view)
        return perm_util.add_user_permission_to_list()
