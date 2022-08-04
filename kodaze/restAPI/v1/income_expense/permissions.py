from rest_framework import permissions
from restAPI.v1.utils.permission_utils import PermissionUtil

class HoldingKassaMedaxilPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingkassamedaxil", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingKassaMexaricPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingkassamexaric", view=view)
        return perm_util.add_user_permission_to_list()

class ShirketKassaMedaxilPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shirketkassamedaxil", view=view)
        return perm_util.add_user_permission_to_list()

class ShirketKassaMexaricPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shirketkassamexaric", view=view)
        return perm_util.add_user_permission_to_list()

class OfisKassaMedaxilPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="ofiskassamedaxil", view=view)
        return perm_util.add_user_permission_to_list()

class OfisKassaMexaricPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="ofiskassamexaric", view=view)
        return perm_util.add_user_permission_to_list()
