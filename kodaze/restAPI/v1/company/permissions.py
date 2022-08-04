from rest_framework import permissions
from restAPI.v1.utils.permission_utils import PermissionUtil

class HoldingPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holding", view=view)
        return perm_util.add_user_permission_to_list()

class ShirketPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shirket", view=view)
        return perm_util.add_user_permission_to_list()

class OfisPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="ofis", view=view)
        return perm_util.add_user_permission_to_list()

    def has_object_permission(self, request, view, obj):
        is_admin = super().has_permission(request, view)
        request_user_shirket = request.user.shirket
        object_shirket = obj.shirket
        print(f"{request_user_shirket=}")
        print(f"{object_shirket=}")

        return request_user_shirket == object_shirket or is_admin

class ShobePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shobe", view=view)
        return perm_util.add_user_permission_to_list()

class VezifelerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="vezifeler", view=view)
        return perm_util.add_user_permission_to_list()

class KomandaPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="komanda", view=view)
        return perm_util.add_user_permission_to_list()

# ******************** Vezifeye gore permission *****************************************
class VezifePermissionPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="vezifepermission", view=view)
        return perm_util.add_user_permission_to_list()
