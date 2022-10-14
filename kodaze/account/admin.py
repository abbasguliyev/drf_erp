from django.contrib import admin
from account.models import (
    CustomerNote, 
    User, 
    Customer, 
    Region,
    EmployeeStatus
)
from django.contrib.auth.models import Permission

class RegionAdmin(admin.ModelAdmin):
    search_fields = (
        "region_ad",
    )

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname")
    list_display_links = ("id", "fullname")

admin.site.register(Customer)
admin.site.register(CustomerNote)

admin.site.register(Region, RegionAdmin)
admin.site.register(EmployeeStatus)

admin.site.register(Permission)