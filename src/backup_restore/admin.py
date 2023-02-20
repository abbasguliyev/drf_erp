from django.contrib import admin
from .models import BackupAndRestore
# Register your models here.

@admin.register(BackupAndRestore)
class BackupAndRestoreAdmin(admin.ModelAdmin):
    list_display = ("id", "backup_date", "restore_date", "media_backup_date")
    list_display_links = ("id",)