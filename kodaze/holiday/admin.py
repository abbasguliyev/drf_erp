from django.contrib import admin

from holiday.models import (
    HoldingGunler,
    IsciGunler,
    KomandaGunler,
    OfisGunler,
    ShirketGunler,
    ShobeGunler,
    VezifeGunler,
    HoldingIstisnaIsci,
    KomandaIstisnaIsci,
    ShirketIstisnaIsci,
    OfisIstisnaIsci,
    ShobeIstisnaIsci,
    VezifeIstisnaIsci
)

# Register your models here.
admin.site.register(HoldingGunler)
admin.site.register(IsciGunler)
admin.site.register(KomandaGunler)
admin.site.register(OfisGunler)
admin.site.register(ShirketGunler)
admin.site.register(ShobeGunler)
admin.site.register(VezifeGunler)
admin.site.register(HoldingIstisnaIsci)
admin.site.register(KomandaIstisnaIsci)
admin.site.register(ShirketIstisnaIsci)
admin.site.register(ShobeIstisnaIsci)
admin.site.register(OfisIstisnaIsci)
admin.site.register(VezifeIstisnaIsci)


