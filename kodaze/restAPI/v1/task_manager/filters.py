import django_filters
from task_manager.models import TaskManager

class TaskManagerFilter(django_filters.FilterSet):
    class Meta:
        model = TaskManager
        date = django_filters.DateFilter(field_name='ishe_baslama_tarixi', input_formats=["%d-%m-%Y"])
        date__gte = django_filters.DateFilter(field_name='ishe_baslama_tarixi', lookup_expr='gte', input_formats=["%d-%m-%Y"])
        date__lte = django_filters.DateFilter(field_name='ishe_baslama_tarixi', lookup_expr='lte', input_formats=["%d-%m-%Y"])
        
        fields = {
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'position': ['exact'],
            'employee': ['exact'],
        }

