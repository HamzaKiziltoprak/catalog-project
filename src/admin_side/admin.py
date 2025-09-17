from django.contrib import admin
from .models import ContactNumber


@admin.register(ContactNumber)
class ContactNumberAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'phone_number')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'phone_number', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')