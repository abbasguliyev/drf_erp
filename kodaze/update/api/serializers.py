from rest_framework import serializers
from core.utils.base_serializer import DynamicFieldsCategorySerializer

from update.models import Update

class UpdateSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Update
        fields = "__all__"
