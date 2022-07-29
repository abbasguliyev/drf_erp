from django.contrib import admin
from .models import (
    Muqavile,
    MuqavileHediyye, 
    OdemeTarix, 
    Deyisim, 
    DemoSatis, 
    MuqavileKreditor
)
class OdemeTarixAdmin(admin.ModelAdmin):
    list_filter = [
        "muqavile",
        'muqavile__odenis_uslubu',
        'odenme_status',
        'gecikdirme_status',
        'buraxilmis_ay_alt_status',
        'natamam_ay_alt_status',
    ]
    search_fields = (
        "muqavile",
    )

# Register your models here.
admin.site.register(Muqavile)
admin.site.register(MuqavileHediyye)
admin.site.register(Deyisim)
admin.site.register(OdemeTarix, OdemeTarixAdmin)
admin.site.register(DemoSatis)
admin.site.register(MuqavileKreditor)