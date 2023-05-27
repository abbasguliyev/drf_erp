from django.contrib import admin
from .models import TaskManager, UserTaskRequest, Advertisement
# Register your models here.
class TaskManagerAdmin(admin.ModelAdmin):
    list_filter = [
        "title",
        'created_date',
        'end_date',
        'position',
        'employee',
        'status',
    ]
    search_fields = (
        "employee__fullname",
    )

admin.site.register(TaskManager, TaskManagerAdmin)
admin.site.register(UserTaskRequest)
admin.site.register(Advertisement)
