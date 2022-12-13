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
@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "company")
    list_display_links = ("id", "name")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")

@admin.register(PermissionForPosition)
class PermissionForPositionAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "permission_group")
    list_display_links = ("id",)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
