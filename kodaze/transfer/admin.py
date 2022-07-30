from django.contrib import admin
from .models import (
    HoldingdenShirketlereTransfer,
    OfisdenShirketeTransfer,
    ShirketdenHoldingeTransfer,
    ShirketdenOfislereTransfer
)
# Register your models here.
admin.site.register(HoldingdenShirketlereTransfer)
admin.site.register(OfisdenShirketeTransfer)
admin.site.register(ShirketdenHoldingeTransfer)
admin.site.register(ShirketdenOfislereTransfer)