import django_filters
from task_manager.models import TaskManager

class TaskManagerFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', input_formats=["%d-%m-%Y"])
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte', input_formats=["%d-%m-%Y"])
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte', input_formats=["%d-%m-%Y"])
    
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

