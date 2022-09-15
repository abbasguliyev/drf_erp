import django_filters
from task_manager.models import TaskManager

class TaskManagerFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFilter(field_name='date', input_formats=["%d-%m-%Y %H:%M:%S"])
    date__gte = django_filters.DateTimeFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y %H:%M:%S"])
    date__lte = django_filters.DateTimeFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y %H:%M:%S"])
    
    class Meta:
        model = TaskManager
        fields = {
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'position': ['exact'],
            'employee': ['exact'],
            'employee__asa': ['exact', 'icontains'],
            'type': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
            'requests': ['exact'],
        }

