from account.models import User
from rest_framework.permissions import IsAdminUser, SAFE_METHODS


class PermissionUtil:
    """
    Login olan userin permissionunun olub olmadigini mueyyen eden class
    """
    __perm_list = set()

    def __init__(self, user: User, request, object_name, view) -> None:
        self.user = user
        self.request = request
        self.object_name = object_name
        self.view = view

    def add_user_permission_to_list(self) -> bool:
        """
        Permissionlara uygun olaraq sorgulari idare eden ve geriye boolean qaytaran method
        """
        is_admin = IsAdminUser.has_permission(
            IsAdminUser, self.request, self.view)

        user = self.user

        try:
            permission_groups = user.app_permission.prefetch_related("groups").values_list('groups__permissions__codename', flat=True)
        except:
            return False
        
        if self.request.method == "POST":
            return (f'add_{self.object_name}' in permission_groups) or is_admin
        elif self.request.method == "PUT":
            return (f'change_{self.object_name}' in permission_groups) or is_admin
        elif self.request.method == "PATCH":
            return (f'change_{self.object_name}' in permission_groups) or is_admin
        elif self.request.method == "DELETE":
            return (f'delete_{self.object_name}' in permission_groups) or is_admin
        elif self.request.method in SAFE_METHODS:
            return (f'view_{self.object_name}' in permission_groups) or is_admin
        else:
            return False
        

class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
