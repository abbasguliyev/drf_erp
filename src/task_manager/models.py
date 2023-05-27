import django
from django.db import models
from django.contrib.auth import get_user_model
from . import  (
    STATUS_CHOICES,
    ICRA_EDILIR
)

User = get_user_model()

class TaskManager(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="given_tasks")
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_date = models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    end_date = models.DateField()
    old_date = models.DateField(null=True, blank=True)
    position = models.ForeignKey(
        "company.Position", on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="gettin_tasks", null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=ICRA_EDILIR, blank=True)

    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_taskmanager", "Tapşırıqlara baxa bilər"),
            ("add_taskmanager", "Tapşırıq əlavə edə bilər"),
            ("change_taskmanager", "Tapşırığı yeniləyə bilər"),
            ("delete_taskmanager", "Tapşırığı silə bilər")
        )

class UserTaskRequest(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="given_requests")
    task = models.ForeignKey(TaskManager, on_delete=models.CASCADE, related_name="requests")
    note = models.TextField()
    change_date = models.DateField(auto_now_add=True)
    new_date = models.DateField()
    is_accept = models.BooleanField(default=False)

class Advertisement(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="given_advertisements")
    title = models.CharField(max_length=250)
    body = models.TextField()
    created_date = models.DateField(default=django.utils.timezone.now, null=True, blank=True)
    position = models.ManyToManyField("company.Position", related_name="advertisements", blank=True)
    
    class Meta:
        ordering = ("-pk",)
        default_permissions = []
        permissions = (
            ("view_advertisement", "Elanlara baxa bilər"),
            ("add_advertisement", "Elan əlavə edə bilər"),
            ("change_advertisement", "Elanı yeniləyə bilər"),
            ("delete_advertisement", "Elanı silə bilər")
        )