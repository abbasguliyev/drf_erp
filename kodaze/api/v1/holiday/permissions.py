from rest_framework import permissions
from api.v1.utils.permission_utils import PermissionUtil
       
class EmployeeWorkingDayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="employeeworkingday", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingWorkingDayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingworkingday", view=view)
        return perm_util.add_user_permission_to_list()

class CompanyWorkingDayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="companyworkingday", view=view)
        return perm_util.add_user_permission_to_list()

class OfficeWorkingDayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officeworkingday", view=view)
        return perm_util.add_user_permission_to_list()

class TeamWorkingDayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="teamworkingday", view=view)
        return perm_util.add_user_permission_to_list()

class PositionWorkingDayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="positionworkingday", view=view)
        return perm_util.add_user_permission_to_list()

class SectionWorkingDayPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="sectionworkingday", view=view)
        return perm_util.add_user_permission_to_list()

class HoldingExceptionWorkerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="holdingexceptionworker", view=view)
        return perm_util.add_user_permission_to_list()

class CompanyExceptionWorkerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="companyexceptionworker", view=view)
        return perm_util.add_user_permission_to_list()

class OfficeExceptionWorkerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="officeexceptionworker", view=view)
        return perm_util.add_user_permission_to_list()

class SectionExceptionWorkerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="sectionexceptionworker", view=view)
        return perm_util.add_user_permission_to_list()

class TeamExceptionWorkerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="teamexceptionworker", view=view)
        return perm_util.add_user_permission_to_list()

class PositionExceptionWorkerPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="positionexceptionworker", view=view)
        return perm_util.add_user_permission_to_list()

class EmployeeArrivalAndDepartureTimesPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        perm_util = PermissionUtil(user=request.user, request=request, object_name="employeearrivalanddeparturetimes", view=view)
        return perm_util.add_user_permission_to_list()