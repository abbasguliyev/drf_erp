from django.contrib import admin
from company.models import (
    Holding, 
    Shirket, 
    Ofis, 
    Shobe, 
    Vezifeler, 
    Komanda, 
    Department,
    VezifePermission, 
) 
# Register your models here.
admin.site.register(Holding)
admin.site.register(Shirket)
admin.site.register(Ofis)
admin.site.register(Shobe)

admin.site.register(Vezifeler)
admin.site.register(Komanda)
admin.site.register(VezifePermission)
admin.site.register(Department)