import django_filters
from task_manager.models import Advertisement, TaskManager, UserTaskRequest

class TaskManagerFilter(django_filters.FilterSet):
    created_date = django_filters.DateFilter(field_name='created_date', input_formats=["%d-%m-%Y"])
    created_date__gte = django_filters.DateFilter(field_name='created_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    created_date__lte = django_filters.DateFilter(field_name='created_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    end_date = django_filters.DateFilter(field_name='end_date', input_formats=["%d-%m-%Y"])
    end_date__gte = django_filters.DateFilter(field_name='end_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    end_date__lte = django_filters.DateFilter(field_name='end_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    old_date = django_filters.DateFilter(field_name='old_date', input_formats=["%d-%m-%Y"])
    old_date__gte = django_filters.DateFilter(field_name='old_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    old_date__lte = django_filters.DateFilter(field_name='old_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    

    class Meta:
        model = TaskManager
        fields = {
            'creator': ['exact'],
            'title': ['exact', 'icontains'],
            'position__name': ['exact'],
            'employee': ['exact'],
            'employee__fullname': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
            'requests': ['exact'],
        }


class UserTaskRequestFilter(django_filters.FilterSet):
    change_date = django_filters.DateFilter(field_name='change_date', input_formats=["%d-%m-%Y"])
    change_date__gte = django_filters.DateFilter(field_name='change_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    change_date__lte = django_filters.DateFilter(field_name='change_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    new_date = django_filters.DateFilter(field_name='new_date', input_formats=["%d-%m-%Y"])
    new_date__gte = django_filters.DateFilter(field_name='new_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    new_date__lte = django_filters.DateFilter(field_name='new_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = UserTaskRequest
        fields = {
            'creator': ['exact'],
            'task': ['exact'],
            'note': ['exact', 'icontains']
        }


class AdvertisementFilter(django_filters.FilterSet):
    created_date = django_filters.DateFilter(field_name='created_date', input_formats=["%d-%m-%Y"])
    created_date__gte = django_filters.DateFilter(field_name='created_date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    created_date__lte = django_filters.DateFilter(field_name='created_date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
    class Meta:
        model = Advertisement
        fields = {
            'creator': ['exact'],
            'title': ['exact', 'icontains'],
            'position__name': ['exact'],
        }

