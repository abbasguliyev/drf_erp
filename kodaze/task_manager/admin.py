from django.contrib import admin
from .models import TaskManager, UserTaskRequest
# Register your models here.
class TaskManagerAdmin(admin.ModelAdmin):
    list_filter = [
        "title",
        'created_date',
        'end_date',
        'position',
        'employee',
        'type',
        'status',
    ]
    search_fields = (
        "employee__asa",
    )

admin.site.register(TaskManager, TaskManagerAdmin)
admin.site.register(UserTaskRequest)
