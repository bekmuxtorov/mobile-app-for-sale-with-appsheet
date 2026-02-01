from django.contrib import admin
from .models import Output


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'customer', 'quantity',
                    'summa', 'is_payment', 'created_at')
    list_filter = ('created_at', 'user', 'is_payment')
    search_fields = ('product__name', 'customer__full_name')
