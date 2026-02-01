from django.contrib import admin
from .models import Input


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'quantity', 'summa', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('product__name',)
