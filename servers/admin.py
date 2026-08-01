from django.contrib import admin
from django.utils.html import format_html

from servers.models import Server


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'ip_address', 'datacenter', 'os', 'status_badge', 'created_at']
    list_filter = ['status', 'os', 'datacenter']
    search_fields = ['hostname', 'ip_address', 'os']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['datacenter']
    fieldsets = (
        ('Server Information', {
            'fields': ('hostname', 'ip_address', 'datacenter')
        }),
        ('System Details', {
            'fields': ('os', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'ONLINE': '#4DFF00',
            'OFFLINE': '#FF0000',
            'MAINTENANCE': '#FFA500'
        }
        color = colors.get(obj.status, '#76B900')
        return format_html(
            '<span style="background-color: {}; color: #0B0B0B; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 12px;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'
