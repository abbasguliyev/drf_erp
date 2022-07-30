from rest_framework import permissions
from restAPI.utils.permission_utils import PermissionUtil
       
class VanLeaderPrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="vanleaderprim", view=view)
        return perm_util.add_user_permission_to_list()

class VanLeaderPrimNewPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="vanleaderprimnew", view=view)
        return perm_util.add_user_permission_to_list()

class DealerPrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="dealerprim", view=view)
        return perm_util.add_user_permission_to_list()

class DealerPrimNewPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="dealerprimnew", view=view)
        return perm_util.add_user_permission_to_list()

class OfficeLeaderPrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officeleaderprim", view=view)
        return perm_util.add_user_permission_to_list()

class CanvasserPrimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="canvasserprim", view=view)
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