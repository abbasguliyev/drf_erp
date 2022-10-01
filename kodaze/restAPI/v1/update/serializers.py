from rest_framework import serializers
from restAPI.core import DynamicFieldsCategorySerializer

from update.models import Update

class UpdateSerializer(DynamicFieldsCategorySerializer):
    class Meta:
        model = Update
        fields = "__all__"
