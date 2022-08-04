from rest_framework import permissions
from restAPI.v1.utils.permission_utils import PermissionUtil


class UserPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="user", view=view)
        return perm_util.add_user_permission_to_list()

class IsciStatusPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="iscistatus", view=view)
        return perm_util.add_user_permission_to_list()

class BolgePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="bolge", view=view)
        return perm_util.add_user_permission_to_list()

class MusteriPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="musteri", view=view)
        return perm_util.add_user_permission_to_list()

class MusteriQeydlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="musteriqeydler", view=view)
        return perm_util.add_user_permission_to_list()

class IsciSatisSayiPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="iscisatissayi", view=view)
        return perm_util.add_user_permission_to_list()

class PermissionModelPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="permission", view=view)
        return perm_util.add_user_permission_to_list()

class GroupPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="group", view=view)
        return perm_util.add_user_permission_to_list()

class PasswordResetPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="passwordreset", view=view)
        return perm_util.add_user_permission_to_list()