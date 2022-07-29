from django.contrib import admin
from .models import (
    Servis, 
    ServisOdeme, 
)

class ServisAdmin(admin.ModelAdmin):
    list_filter = [
        "muqavile",
    ]
    search_fields = (
        "muqavile",
    )

class ServisOdemeAdmin(admin.ModelAdmin):
    list_filter = [
        "servis",
    ]
    search_fields = (
        "servis",
    )

admin.site.register(Servis, ServisAdmin)
admin.site.register(ServisOdeme, ServisOdemeAdmin)