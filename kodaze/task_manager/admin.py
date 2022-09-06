from django.contrib import admin
from .models import TaskManager, UserTaskRequest
# Register your models here.

admin.site.register(TaskManager)
admin.site.register(UserTaskRequest)
