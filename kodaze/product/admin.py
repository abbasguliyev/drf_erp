from django.contrib import admin
from .models import Product, Category, UnitOfMeasure

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UnitOfMeasure)
