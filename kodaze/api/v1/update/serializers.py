from rest_framework import serializers
from api.core import DynamicFieldsCategorySerializer

from update.models import Update

class UpdateSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Update
        fields = "__all__"
