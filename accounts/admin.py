from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Personal', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email'),
        }),
        ('Authorization Information', {
            'classes': ('collapse',),
            'fields': ('phone_number', 'password',),
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_phone_confirmed', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Status', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )

    list_display = (
        'phone_number', 
        'first_name', 
        'last_name', 
        'is_staff'
    )

    list_filter = (
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'groups'
    )

    search_fields = (
        'phone_number',
    )

    filter_horizontal = (
        'groups', 
        'user_permissions',
    )

    ordering = ('-created',)

    save_on_top = True
