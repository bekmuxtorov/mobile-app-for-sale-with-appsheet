from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'full_name', 'is_staff', 'is_active')
    search_fields = ('phone_number', 'full_name')
    ordering = ('phone_number',)

    # Since we removed username, we need to adjust fieldsets if necessary or stick to default
    # But UserAdmin expects username usually.
    # Let's keep it simple for now, or minimal custom config if needed.
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'full_name', 'password'),
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'created_at')
    search_fields = ('full_name', 'phone_number')
