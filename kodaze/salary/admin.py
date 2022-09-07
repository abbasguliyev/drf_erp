from django.contrib import admin
from .models import (
    Avans, 
    Bonus, 
    Menecer2Prim, 
    Menecer1PrimNew, 
    Kesinti, 
    MaasGoruntuleme,
    GroupLeaderPrimNew, 
    MaasOde, 
    KreditorPrim, 
    OfficeLeaderPrim
)
# Register your models here.

class MaasGoruntulemeAdmin(admin.ModelAdmin):
    search_fields = (
        "isci__id",
        "isci__asa",
        
    )
    list_filter = [
        "isci__id",
        "tarix"
    ]

admin.site.register(Avans)
admin.site.register(Bonus)
admin.site.register(Menecer2Prim)
admin.site.register(Menecer1PrimNew)
admin.site.register(Kesinti)
admin.site.register(MaasGoruntuleme, MaasGoruntulemeAdmin)
admin.site.register(GroupLeaderPrimNew)
admin.site.register(MaasOde)
admin.site.register(KreditorPrim)
admin.site.register(OfficeLeaderPrim)

