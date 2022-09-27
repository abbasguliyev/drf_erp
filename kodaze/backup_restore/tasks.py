import datetime

from celery import shared_task

from django.conf import settings
from django.core.management import call_command

from . models import BackupAndRestore

def return_date(str_date:str) -> datetime.date:
    date = datetime.datetime.strptime(f"{str_date.day}-{str_date.month}-{str_date.year}", '%d-%m-%Y')
    return date

@shared_task(name='backup')
def backup():
    if settings.DEBUG is True:
        return f"Could not be backed up: Debug is True"
    try:
        call_command("dbbackup")
        try:
            backup = BackupAndRestore.objects.all().last()
            backup.backup_date = return_date(f"{datetime.date.today().day}-{datetime.date.today().month}-{datetime.date.today().year}")
            backup.save()
        except:
            backup = BackupAndRestore.objects.create(
                backup_date = return_date(f"{datetime.date.today().day}-{datetime.date.today().month}-{datetime.date.today().year}")
            )
            backup.save()
        return f"Backed up successfully: {datetime.date.today().day}-{datetime.date.today().month}-{datetime.date.today().year}"
    except:
        return f"Could not be backed up: {datetime.date.today().day}-{datetime.date.today().month}-{datetime.date.today().year}"

@shared_task(name='mediabackup')
def mediabackup():
    if settings.DEBUG is True:
        return f"Could not be backed up: Debug is True"
    try:
        call_command("mediabackup", "--output-filename=media.zip")
        try:
            backup = BackupAndRestore.objects.all().last()
            backup.media_backup_date = return_date(f"{datetime.date.today().day}-{datetime.date.today().month}-{datetime.date.today().year}")
            backup.save()
        except:
            backup = BackupAndRestore.objects.create(
                media_backup_date = return_date(f"{datetime.date.today().day}-{datetime.date.today().month}-{datetime.date.today().year}")
            )
            backup.save()
        return f"Backed up successfully: {datetime.date.today().day}-{datetime.date.today().month}-{datetime.date.today().year}"
    except:
        return f"Could not be backed up: {datetime.date.today().day}-{datetime.date.today().month}-{datetime.date.today().year}"