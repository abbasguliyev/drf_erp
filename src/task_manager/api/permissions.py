from rest_framework import permissions
from core.utils.permission_utils import PermissionUtil

class TaskManagerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="taskmanager", view=view)
        return perm_util.add_user_permission_to_list()

class TaskManagerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="taskmanager", view=view)
        return perm_util.add_user_permission_to_list()

class AdvertisementPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="advertisement", view=view)
        return perm_util.add_user_permission_to_list()
