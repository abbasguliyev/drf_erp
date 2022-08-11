from django.db import models

# Create your models here.
class BackupAndRestore(models.Model):
    backup_date = models.DateField(null=True, blank=True)
    restore_date = models.DateField(null=True, blank=True)
    media_backup_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_backupandrestore", "Mövcud `backup and restore`lara baxa bilər"),
            ("add_backupandrestore", "`Backup and restore` əlavə edə bilər"),
            ("change_backupandrestore", "`Backup and restore` məlumatlarını yeniləyə bilər"),
            ("delete_backupandrestore", "`Backup and restore` silə bilər")
        )