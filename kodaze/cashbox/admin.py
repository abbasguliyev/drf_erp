from django.contrib import admin
from cashbox.models import (
    OfisKassa,
    ShirketKassa,
    HoldingKassa,
    PulAxini
)
# Register your models here.
admin.site.register(OfisKassa)
admin.site.register(ShirketKassa)
admin.site.register(HoldingKassa)
admin.site.register(PulAxini)
