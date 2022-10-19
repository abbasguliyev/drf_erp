from account.models import User
from rest_framework.permissions import IsAdminUser, SAFE_METHODS


class PermissionUtil:
    """
    Login olan userin permissionunun olub olmadigini mueyyen eden class
    """
    __perm_list = list()

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
        permission_groups = user.groups.all()
        for permission_group in permission_groups:
            all_permissions = permission_group.permissions.all()
            for perm in all_permissions:
                self.__perm_list.append(perm.codename)

        user_permissions = user.user_permissions.all()
        for user_permission in user_permissions:
            if user_permission not in self.__perm_list:
                self.__perm_list.append(user_permission.codename)

        if self.request.method == "POST":
            return f'add_{self.object_name}' in self.__perm_list or is_admin
        elif self.request.method == "PUT":
            return f'change_{self.object_name}' in self.__perm_list or is_admin
        elif self.request.method == "PATCH":
            return f'change_{self.object_name}' in self.__perm_list or is_admin
        elif self.request.method == "DELETE":
            return f'delete_{self.object_name}' in self.__perm_list or is_admin
        elif self.request.method in SAFE_METHODS:
            return f'view_{self.object_name}' in self.__perm_list or is_admin
        else:
            return False


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
