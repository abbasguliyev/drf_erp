import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from django.core.management import call_command
import datetime
from backup_restore.models import BackupAndRestore
from backup_restore.api.serializers import BackupAndRestoreSerializer


class BackupAndRestoreAPIView(generics.ListAPIView):
    queryset = BackupAndRestore.objects.all()
    serializer_class = BackupAndRestoreSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
@permission_classes([IsAdminUser])
def back_up(request):
    if request.method == "POST":
        if settings.DEBUG is True:
            return Response({'detail': f"Could not be backed up: Debug is True"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            call_command("dbbackup")
            try:
                backup = BackupAndRestore.objects.all().last()
                backup.backup_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                backup.save()
            except:
                backup = BackupAndRestore.objects.create(
                    backup_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                )
                backup.save()
            return Response({'detail': f"Backup yerinə yetirildi: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"}, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response({'detail': f"Backup zamanı xəta baş verdi: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def media_back_up(request):
    if request.method == "POST":
        if settings.DEBUG is True:
            return Response({'detail': f"Could not be backed up: Debug is True"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            call_command("mediabackup", "--output-filead=media.zip")
            try:
                backup = BackupAndRestore.objects.all().last()
                backup.media_backup_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                backup.save()
            except:
                backup = BackupAndRestore.objects.create(
                    media_backup_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                )
                backup.save()
            return Response({'detail': f"Media Backup yerinə yetirildi: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"}, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response({'detail': f"Backup zamanı xəta baş verdi: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def restore(request):
    if request.method == "POST":
        if settings.DEBUG is True:
            return Response({'detail': f"Could not be restore: Debug is True"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            call_command("dbrestore", "--noinput")
            try:
                backup = BackupAndRestore.objects.all().last()
                backup.restore_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                backup.save()
            except:
                backup = BackupAndRestore.objects.create(
                    restore_date =  f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"
                )
                backup.save()
            return Response({'detail': f"Restore yerinə yetirildi: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"}, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response({'detail': f"Backup zamanı xəta baş verdi: {datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}"}, status=status.HTTP_400_BAD_REQUEST)
