from rest_framework import permissions
from restAPI.v1.utils.permission_utils import PermissionUtil
       
class GroupLeaderPrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="group_leaderprim", view=view)
        return perm_util.add_user_permission_to_list()

class GroupLeaderPrimNewPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="group_leaderprimnew", view=view)
        return perm_util.add_user_permission_to_list()

class Menecer1PrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="menecer1prim", view=view)
        return perm_util.add_user_permission_to_list()

class Menecer1PrimNewPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="menecer1primnew", view=view)
        return perm_util.add_user_permission_to_list()

class OfficeLeaderPrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officeleaderprim", view=view)
        return perm_util.add_user_permission_to_list()

class Menecer2PrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="menecer2prim", view=view)
        return perm_util.add_user_permission_to_list()

class AvansPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="avans", view=view)
        return perm_util.add_user_permission_to_list()

class KesintiPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="kesinti", view=view)
        return perm_util.add_user_permission_to_list()

class BonusPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="bonus", view=view)
        return perm_util.add_user_permission_to_list()

class MaasGoruntulemePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="maasgoruntuleme", view=view)
        return perm_util.add_user_permission_to_list()

class MaasOdePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="maasode", view=view)
        return perm_util.add_user_permission_to_list()

class KreditorPrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="kreditorprim", view=view)
        return perm_util.add_user_permission_to_list()