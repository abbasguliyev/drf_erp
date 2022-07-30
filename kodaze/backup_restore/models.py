from django.db import models

# Create your models here.
class BackupAndRestore(models.Model):
    backup_date = models.DateField(null=True, blank=True)
    restore_date = models.DateField(null=True, blank=True)
    media_backup_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("-pk",)