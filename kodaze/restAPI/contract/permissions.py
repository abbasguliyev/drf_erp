from rest_framework import permissions
from restAPI.utils.permission_utils import PermissionUtil


class MuqavilePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="muqavile", view=view)
        return perm_util.add_user_permission_to_list()

class DeyisimPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="deyisim", view=view)
        return perm_util.add_user_permission_to_list()

class OdemeTarixleriPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="odemetarix", view=view)
        return perm_util.add_user_permission_to_list()

class MuqavileHediyyePermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="muqavilehediyye", view=view)
        return perm_util.add_user_permission_to_list()

class DemoSatisPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="demosatis", view=view)
        return perm_util.add_user_permission_to_list()

class MuqavileKreditorPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="muqavilekreditor", view=view)
        return perm_util.add_user_permission_to_list()