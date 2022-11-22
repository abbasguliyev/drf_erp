import django_filters

from update.models import Update

class UpdateFilter(django_filters.FilterSet):
    class Meta:
        model = Update
        fields = {
            'update_name': ['exact', 'icontains'],
            'update_description': ['exact', 'icontains'],
            'update_version': ['exact', 'icontains'],
        }

