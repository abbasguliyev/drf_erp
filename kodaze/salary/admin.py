from django.contrib import admin
from .models import (
    Avans, 
    Bonus, 
    CanvasserPrim, 
    DealerPrimNew, 
    Kesinti, 
    MaasGoruntuleme,
    VanLeaderPrimNew, 
    MaasOde, 
    KreditorPrim, 
    OfficeLeaderPrim
)
# Register your models here.

admin.site.register(Avans)
admin.site.register(Bonus)
admin.site.register(CanvasserPrim)
admin.site.register(DealerPrimNew)
admin.site.register(Kesinti)
admin.site.register(MaasGoruntuleme)
admin.site.register(VanLeaderPrimNew)
admin.site.register(MaasOde)
admin.site.register(KreditorPrim)
admin.site.register(OfficeLeaderPrim)

