from rest_framework import permissions
from restAPI.utils.permission_utils import PermissionUtil
       
class IsciGunlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="iscigunler", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingGunlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdinggunler", view=view)
        return perm_util.add_user_permission_to_list()

class ShirketGunlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shirketgunler", view=view)
        return perm_util.add_user_permission_to_list()

class OfisGunlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="ofisgunler", view=view)
        return perm_util.add_user_permission_to_list()

class KomandaGunlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="komandagunler", view=view)
        return perm_util.add_user_permission_to_list()

class VezifeGunlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="vezifegunler", view=view)
        return perm_util.add_user_permission_to_list()

class ShobeGunlerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shobegunler", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingIstisnaIsciPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingistisnaisci", view=view)
        return perm_util.add_user_permission_to_list()

class ShirketIstisnaIsciPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shirketistisnaisci", view=view)
        return perm_util.add_user_permission_to_list()

class OfisIstisnaIsciPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="ofisistisnaisci", view=view)
        return perm_util.add_user_permission_to_list()

class ShobeIstisnaIsciPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="shobeistisnaisci", view=view)
        return perm_util.add_user_permission_to_list()

class KomandaIstisnaIsciPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="komandaistisnaisci", view=view)
        return perm_util.add_user_permission_to_list()

class VezifeIstisnaIsciPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="vezifeistisnaisci", view=view)
        return perm_util.add_user_permission_to_list()

class IsciGelibGetmeVaxtlariPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="iscigelibgetmevaxtlari", view=view)
        return perm_util.add_user_permission_to_list()