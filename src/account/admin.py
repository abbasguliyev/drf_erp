from django.contrib import admin
from account.models import (
    User, 
    Customer, 
    Region,
    EmployeeStatus,
    EmployeeActivity
)
from django.contrib.auth.models import Permission

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "region_name")
    search_fields = ("region_name",)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "fullname")
    list_display_links = ("id", "username")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "is_active")
    list_display_links = ("id", "fullname")

@admin.register(EmployeeStatus)
class EmployeeStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status_name")
    list_display_links = ("id", "status_name")

@admin.register(EmployeeActivity)
class EmployeeActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "status")
    list_display_links = ("id", "employee", "status")

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_per_page = 350
    list_display = ("id", "name", "content_type", "codename")
    list_display_links = ("id", "name")