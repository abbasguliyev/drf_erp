import django
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class TaskManager(models.Model):
    ICRA_EDILIR = "İcra edilir"
    GECIKIR = "Gecikir"
    TAMAMLANDI = "Tamamlandı"
    STATUS_CHOICES = [
        (ICRA_EDILIR, 'İcra edilir'),
        (GECIKIR, 'Gecikir'),
        (TAMAMLANDI, 'Tamamlandı'),
    ]
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_date = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)
    end_date = models.DateTimeField()
    position = models.ForeignKey(
        "company.Vezifeler", on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
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

class UserTaskRequest(models.Model):
    task = models.ForeignKey(TaskManager, on_delete=models.CASCADE, related_name="requests")
    note = models.TextField()
    change_date = models.DateField(auto_now_add=True)
    new_date = models.DateField()

class Advertisement(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_date = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)
    position = models.ForeignKey(
        "company.Vezifeler", on_delete=models.CASCADE, related_name="advertisements", null=True, blank=True)
    
    class Meta:
        ordering = ("pk",)
        default_permissions = []
        permissions = (
            ("view_advertisement", "Elanlara baxa bilər"),
            ("add_advertisement", "Elan əlavə edə bilər"),
            ("change_advertisement", "Elanı yeniləyə bilər"),
            ("delete_advertisement", "Elanı silə bilər")
        )