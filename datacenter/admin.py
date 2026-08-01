from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from datacenter.models import Datacenter


@admin.register(Datacenter)
class DatacenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'country', 'city', 'tier', 'server_count', 'created_at']
    list_filter = ['tier', 'provider', 'country', 'city']
    search_fields = ['name', 'provider', 'country', 'city']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'provider', 'tier')
        }),
        ('Location', {
            'fields': ('country', 'city', 'latitude', 'longitude')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def server_count(self, obj):
        count = obj.servers.count()
        return format_html('<span style="color: #76B900; font-weight: bold;">{}</span>', count)
    server_count.short_description = 'Servers'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(server_count=Count('servers'))