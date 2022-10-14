from django.contrib import admin
from company.models import (
    Holding, 
    Company, 
    Office, 
    Section, 
    Position, 
    Team, 
    Department,
    PermissionForPosition, 
) 
# Register your models here.
admin.site.register(Holding)
admin.site.register(Company)
admin.site.register(Office)
admin.site.register(Section)

admin.site.register(Team)
admin.site.register(PermissionForPosition)
admin.site.register(Department)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
