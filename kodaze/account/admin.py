from django.contrib import admin
from account.models import (
    CustomerNote, 
    User, 
    Customer, 
    Region,
    EmployeeStatus
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


admin.site.register(CustomerNote)
admin.site.register(EmployeeStatus)
admin.site.register(Permission)