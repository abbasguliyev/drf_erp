from rest_framework import serializers
from backup_restore.models import BackupAndRestore

class BackupAndRestoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupAndRestore
        fields = "__all__"