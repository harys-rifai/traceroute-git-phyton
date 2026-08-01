from django.contrib import admin
from django.utils.html import format_html

from .models import Traceroute, TracerouteHop, WANStatus, WirelessStatus, LANStatus, OpticalStatus, VoIPStatus


@admin.register(Traceroute)
class TracerouteAdmin(admin.ModelAdmin):
    list_display = ['target', 'status_badge', 'source_ip', 'created_by', 'created_at']
    list_filter = ['status', 'created_at', 'created_by']
    search_fields = ['target', 'source_ip', 'created_by__email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Target Information', {
            'fields': ('target', 'source_ip')
        }),
        ('Status', {
            'fields': ('status', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'PENDING': '#FFA500',
            'RUNNING': '#76B900',
            'COMPLETED': '#4DFF00',
            'FAILED': '#FF0000'
        }
        color = colors.get(obj.status, '#76B900')
        return format_html(
            '<span style="background-color: {}; color: #0B0B0B; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 12px;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'


@admin.register(TracerouteHop)
class TracerouteHopAdmin(admin.ModelAdmin):
    list_display = ['traceroute', 'hop_number', 'ip_address', 'hostname', 'latency_display', 'country', 'city']
    list_filter = ['traceroute', 'country']
    search_fields = ['ip_address', 'hostname', 'country', 'city', 'asn']
    ordering = ['traceroute', 'hop_number']
    autocomplete_fields = ['traceroute']

    def latency_display(self, obj):
        if obj.latency is None:
            return '-'
        return format_html('<span style="color: #4DFF00;">{} ms</span>', obj.latency)
    latency_display.short_description = 'Latency'


@admin.register(WANStatus)
class WANStatusAdmin(admin.ModelAdmin):
    list_display = ['wan_index', 'state_badge', 'ip_address', 'connection_type', 'gateway', 'created_at']
    list_filter = ['state', 'connection_type', 'created_at']
    search_fields = ['ip_address', 'gateway', 'wan_mac', 'connection_type']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('WAN Connection', {
            'fields': ('wan_index', 'state', 'mode', 'ip_type', 'connection_type')
        }),
        ('IPv4 Settings', {
            'fields': ('ip_address', 'subnet_mask', 'dns_server', 'gateway')
        }),
        ('VLAN', {
            'fields': ('vlan_id', 'priority')
        }),
        ('MAC & Uptime', {
            'fields': ('wan_mac', 'connection_uptime')
        }),
        ('IPv6 Settings', {
            'fields': ('ipv6_status', 'ipv6_address', 'ipv6_prefix', 'ipv6_gateway', 'ipv6_primary_dns', 'ipv6_secondary_dns'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def state_badge(self, obj):
        colors = {
            'Up': '#4DFF00',
            'Down': '#FF0000',
            'Idle': '#FFA500',
            'Unknown': '#9ca3af',
        }
        color = colors.get(obj.state, '#76B900')
        return format_html(
            '<span style="background-color: {}; color: #0B0B0B; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 12px;">{}</span>',
            color, obj.state
        )
    state_badge.short_description = 'State'


@admin.register(WirelessStatus)
class WirelessStatusAdmin(admin.ModelAdmin):
    list_display = ['ssid', 'wifi_state', 'channel', 'signal_strength', 'created_at']
    list_filter = ['wifi_state', 'channel', 'created_at']
    search_fields = ['ssid', 'bssid', 'security_mode']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LANStatus)
class LANStatusAdmin(admin.ModelAdmin):
    list_display = ['lan_ip', 'lan_mask', 'dhcp_enabled', 'num_clients', 'created_at']
    list_filter = ['dhcp_enabled', 'created_at']
    search_fields = ['lan_ip', 'lan_mac']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OpticalStatus)
class OpticalStatusAdmin(admin.ModelAdmin):
    list_display = ['tx_power', 'rx_power', 'optical_state', 'temperature', 'created_at']
    list_filter = ['optical_state', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VoIPStatus)
class VoIPStatusAdmin(admin.ModelAdmin):
    list_display = ['voip_state', 'registration_state', 'active_calls', 'created_at']
    list_filter = ['voip_state', 'registration_state', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']