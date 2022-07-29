from django.contrib import admin
from .models import (
    HoldingKassaMedaxil,
    HoldingKassaMexaric,
    OfisKassaMedaxil,
    OfisKassaMexaric,
    ShirketKassaMedaxil,
    ShirketKassaMexaric
) 
# Register your models here.
admin.site.register(HoldingKassaMedaxil)
admin.site.register(HoldingKassaMexaric)
admin.site.register(OfisKassaMedaxil)
admin.site.register(OfisKassaMexaric)
admin.site.register(ShirketKassaMedaxil)
admin.site.register(ShirketKassaMexaric)
