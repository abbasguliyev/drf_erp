import datetime

from celery import shared_task

from django.conf import settings
from django.core.management import call_command

from backup_restore.models import BackupAndRestore

indi = datetime.date.today()

@shared_task(name='backup')
def backup():
    if settings.DEBUG is True:
        return f"Could not be backed up: Debug is True"
    try:
        call_command("dbbackup")
        try:
            backup = BackupAndRestore.objects.all().last()
            backup.backup_date = f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
            backup.save()
        except:
            backup = BackupAndRestore.objects.create(
                backup_date = f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
            )
            backup.save()
        return f"Backed up successfully: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
    except:
        return f"Could not be backed up: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"

@shared_task(name='mediabackup')
def mediabackup():
    if settings.DEBUG is True:
        return f"Could not be backed up: Debug is True"
    try:
        call_command("mediabackup", "--output-filename=media.zip")
        try:
            backup = BackupAndRestore.objects.all().last()
            backup.media_backup_date = f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
            backup.save()
        except:
            backup = BackupAndRestore.objects.create(
                media_backup_date = f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
            )
            backup.save()
        return f"Backed up successfully: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
    except:
        return f"Could not be backed up: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"