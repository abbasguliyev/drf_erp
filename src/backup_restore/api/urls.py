from django.urls import path
from backup_restore.api import views as backup_views

urlpatterns = [
    path('', backup_views.back_up),
    path('restore/', backup_views.restore),
    path('media-backup/', backup_views.media_back_up),
    path('get-backup/', backup_views.BackupAndRestoreAPIView.as_view()),
]