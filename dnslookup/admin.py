from django.contrib import admin
from django.utils.html import format_html

from .models import DnsQuery


@admin.register(DnsQuery)
class DnsQueryAdmin(admin.ModelAdmin):
    list_display = ['domain', 'record_type_badge', 'resolver', 'ttl_display', 'created_by', 'created_at']
    list_filter = ['record_type', 'created_at', 'created_by']
    search_fields = ['domain', 'result', 'resolver']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Query Information', {
            'fields': ('domain', 'record_type', 'resolver', 'ttl')
        }),
        ('Result', {
            'fields': ('result',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def record_type_badge(self, obj):
        colors = {
            'A': '#4DFF00',
            'AAAA': '#76B900',
            'MX': '#00BFFF',
            'TXT': '#FFA500',
            'SPF': '#FFA500',
            'CNAME': '#FF69B4',
            'NS': '#9370DB',
            'PTR': '#FFD700'
        }
        color = colors.get(obj.record_type, '#76B900')
        return format_html(
            '<span style="background-color: {}; color: #0B0B0B; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 12px;">{}</span>',
            color, obj.record_type
        )
    record_type_badge.short_description = 'Type'

    def ttl_display(self, obj):
        if obj.ttl is None:
            return '-'
        return format_html('<span style="color: #76B900;">{} s</span>', obj.ttl)
    ttl_display.short_description = 'TTL'
