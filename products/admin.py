from django.contrib import admin
from .models import Unit, Product, Category


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'price', 'stock_quantity')
    list_filter = ('category', 'unit')
    search_fields = ('name',)
