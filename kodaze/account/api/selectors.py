from django.db.models.query import QuerySet
from account.models import EmployeeStatus, Customer, Region
from django.contrib.auth import get_user_model

User = get_user_model()

def user_list(*, filters=None) -> QuerySet[User]:
    filters = filters or {}
    qs = User.objects.select_related(
                'company', 'office', 'department', 'position', 'region', 'employee_status', 'commission',
            ).prefetch_related('user_permissions', 'groups').all()
    return qs

def customer_list(*, filters=None) -> QuerySet[Customer]:
    filters = filters or {}
    qs = Customer.objects.select_related('region').all()
    return qs

def employee_status_list(*, filters=None) -> QuerySet[EmployeeStatus]:
    filters = filters or {}
    qs = EmployeeStatus.objects.all()
    return qs

def region_list(*, filters=None) -> QuerySet[Region]:
    filters = filters or {}
    qs = Region.objects.all()
    return qs