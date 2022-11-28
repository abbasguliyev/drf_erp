from rest_framework import permissions
from core.utils.permission_utils import PermissionUtil
       
class EmployeeWorkingDayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="employeeworkingday", view=view)
        return perm_util.add_user_permission_to_list()

class EmployeeHolidayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="employeeholiday", view=view)
        return perm_util.add_user_permission_to_list()

class EmployeeHolidayHistoryPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="employeeholidayhistory", view=view)
        return perm_util.add_user_permission_to_list()

class HolidayOperationPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holidayoperation", view=view)
        return perm_util.add_user_permission_to_list()