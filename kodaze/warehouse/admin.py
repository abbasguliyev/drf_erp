from django.contrib import admin
from .models import Anbar, Stok, AnbarQeydler, Emeliyyat

# Register your models here.
admin.site.register(Anbar)
admin.site.register(AnbarQeydler)
admin.site.register(Emeliyyat)
admin.site.register(Stok)