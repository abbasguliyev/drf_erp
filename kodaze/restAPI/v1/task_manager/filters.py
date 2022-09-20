import django_filters
from task_manager.models import Advertisement, TaskManager, UserTaskRequest

class TaskManagerFilter(django_filters.FilterSet):
    created_date = django_filters.DateTimeFilter(field_name='created_date', input_formats=["%d-%m-%Y %H:%M:%S"])
    created_date__gte = django_filters.DateTimeFilter(field_name='created_date', lookup_expr='gte', input_formats=["%d-%m-%Y %H:%M:%S"])
    created_date__lte = django_filters.DateTimeFilter(field_name='created_date', lookup_expr='lte', input_formats=["%d-%m-%Y %H:%M:%S"])
    
    end_date = django_filters.DateTimeFilter(field_name='end_date', input_formats=["%d-%m-%Y %H:%M:%S"])
    end_date__gte = django_filters.DateTimeFilter(field_name='end_date', lookup_expr='gte', input_formats=["%d-%m-%Y %H:%M:%S"])
    end_date__lte = django_filters.DateTimeFilter(field_name='end_date', lookup_expr='lte', input_formats=["%d-%m-%Y %H:%M:%S"])
    
    class Meta:
        model = TaskManager
        fields = {
            'title': ['exact', 'icontains'],
            'position__vezife_adi': ['exact'],
            # 'employee': ['exact'],
            'employee__asa': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
            'requests': ['exact'],
        }


class UserTaskRequestFilter(django_filters.FilterSet):
    change_date = django_filters.DateTimeFilter(field_name='change_date', input_formats=["%d-%m-%Y %H:%M:%S"])
    change_date__gte = django_filters.DateTimeFilter(field_name='change_date', lookup_expr='gte', input_formats=["%d-%m-%Y %H:%M:%S"])
    change_date__lte = django_filters.DateTimeFilter(field_name='change_date', lookup_expr='lte', input_formats=["%d-%m-%Y %H:%M:%S"])
    
    new_date = django_filters.DateTimeFilter(field_name='new_date', input_formats=["%d-%m-%Y %H:%M:%S"])
    new_date__gte = django_filters.DateTimeFilter(field_name='new_date', lookup_expr='gte', input_formats=["%d-%m-%Y %H:%M:%S"])
    new_date__lte = django_filters.DateTimeFilter(field_name='new_date', lookup_expr='lte', input_formats=["%d-%m-%Y %H:%M:%S"])
    
    class Meta:
        model = UserTaskRequest
        fields = {
            'task': ['exact'],
            'note': ['exact', 'icontains']
        }


class AdvertisementFilter(django_filters.FilterSet):
    created_date = django_filters.DateTimeFilter(field_name='created_date', input_formats=["%d-%m-%Y %H:%M:%S"])
    created_date__gte = django_filters.DateTimeFilter(field_name='created_date', lookup_expr='gte', input_formats=["%d-%m-%Y %H:%M:%S"])
    created_date__lte = django_filters.DateTimeFilter(field_name='created_date', lookup_expr='lte', input_formats=["%d-%m-%Y %H:%M:%S"])
    
    class Meta:
        model = Advertisement
        fields = {
            'title': ['exact', 'icontains'],
            'position__vezife_adi': ['exact'],
        }

