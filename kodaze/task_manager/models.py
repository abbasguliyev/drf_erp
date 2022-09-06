import django
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class TaskManager(models.Model):
    TAPSIRIQ = 'tapşırıq'
    ELAN = 'elan'
    ICRA_EDILIR = "İcra edilir"
    GECIKIR = "Gecikir"
    TAMAMLANDI = "Tamamlandı"
    TYPE_CHOICES = [
        (TAPSIRIQ, 'tapşırıq'),
        (ELAN, 'elan'),
    ]
    STATUS_CHOICES = [
        (ICRA_EDILIR, 'İcra edilir'),
        (GECIKIR, 'Gecikir'),
        (TAMAMLANDI, 'Tamamlandı'),
    ]
    title = models.CharField(max_length=250)
    description = models.TextField()
    document = models.FileField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)
    position = models.ForeignKey(
        "company.Vezifeler", on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default=None, null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=ICRA_EDILIR, blank=True)

    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_taskmanager", "Tapşırıqlara baxa bilər"),
            ("add_taskmanager", "Tapşırıq əlavə edə bilər"),
            ("change_taskmanager", "Tapşırığı yeniləyə bilər"),
            ("delete_taskmanager", "Tapşırığı silə bilər")
        )

    def __str__(self) -> str:
        return self.title

class UserTaskRequest(models.Model):
    task = models.ForeignKey(TaskManager, on_delete=models.CASCADE, related_name="requests")
    note = models.TextField()