from django.db import models
from core.models import BaseModel
from accounts.models import CustomUser


STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('RUNNING', 'Running'),
    ('COMPLETED', 'Completed'),
    ('FAILED', 'Failed'),
)


class Traceroute(BaseModel):
    target = models.CharField(max_length=255)
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='traceroutes',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Traceroute to {self.target}"


class TracerouteHop(models.Model):
    traceroute = models.ForeignKey(
        Traceroute,
        on_delete=models.CASCADE,
        related_name='hops',
    )
    hop_number = models.PositiveIntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    hostname = models.CharField(max_length=255, null=True, blank=True)
    latency = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    asn = models.CharField(max_length=50, null=True, blank=True)

    loss = models.FloatField(null=True, blank=True)
    min_rtt = models.FloatField(null=True, blank=True)
    max_rtt = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['hop_number']

    def __str__(self):
        return f"Hop {self.hop_number}: {self.ip_address}"


class WANStatus(BaseModel):
    wan_index = models.PositiveIntegerField(default=1)
    state = models.CharField(max_length=20, default='Unknown')
    mode = models.CharField(max_length=50, null=True, blank=True)
    ip_type = models.CharField(max_length=20, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    subnet_mask = models.GenericIPAddressField(null=True, blank=True)
    dns_server = models.GenericIPAddressField(null=True, blank=True)
    vlan_id = models.PositiveIntegerField(null=True, blank=True)
    priority = models.PositiveIntegerField(null=True, blank=True)
    connection_type = models.CharField(max_length=50, null=True, blank=True)
    wan_mac = models.CharField(max_length=17, null=True, blank=True)
    connection_uptime = models.CharField(max_length=50, null=True, blank=True)
    gateway = models.GenericIPAddressField(null=True, blank=True)
    ipv6_status = models.CharField(max_length=20, null=True, blank=True)
    ipv6_address = models.GenericIPAddressField(null=True, blank=True)
    ipv6_prefix = models.CharField(max_length=64, null=True, blank=True)
    ipv6_gateway = models.GenericIPAddressField(null=True, blank=True)
    ipv6_primary_dns = models.GenericIPAddressField(null=True, blank=True)
    ipv6_secondary_dns = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'WAN Status'
        verbose_name_plural = 'WAN Status'

    def __str__(self):
        return f"WAN {self.wan_index}: {self.state} - {self.ip_address}"


class WirelessStatus(BaseModel):
    ssid = models.CharField(max_length=255, null=True, blank=True)
    bssid = models.CharField(max_length=17, null=True, blank=True)
    channel = models.PositiveIntegerField(null=True, blank=True)
    channel_width = models.CharField(max_length=20, null=True, blank=True)
    security_mode = models.CharField(max_length=50, null=True, blank=True)
    signal_strength = models.IntegerField(null=True, blank=True)
    tx_rate = models.FloatField(null=True, blank=True)
    rx_rate = models.FloatField(null=True, blank=True)
    associated_clients = models.PositiveIntegerField(null=True, blank=True)
    wifi_state = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wireless Status'
        verbose_name_plural = 'Wireless Status'

    def __str__(self):
        return f"Wireless: {self.ssid or 'N/A'} - {self.wifi_state or 'Unknown'}"


class LANStatus(BaseModel):
    lan_ip = models.GenericIPAddressField(null=True, blank=True)
    lan_mask = models.GenericIPAddressField(null=True, blank=True)
    dhcp_enabled = models.BooleanField(default=False)
    dhcp_start = models.GenericIPAddressField(null=True, blank=True)
    dhcp_end = models.GenericIPAddressField(null=True, blank=True)
    dhcp_lease_time = models.CharField(max_length=50, null=True, blank=True)
    lan_mac = models.CharField(max_length=17, null=True, blank=True)
    num_clients = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'LAN Status'
        verbose_name_plural = 'LAN Status'

    def __str__(self):
        return f"LAN: {self.lan_ip or 'N/A'} ({self.num_clients or 0} clients)"


class OpticalStatus(BaseModel):
    tx_power = models.FloatField(null=True, blank=True)
    rx_power = models.FloatField(null=True, blank=True)
    tx_bias = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    voltage = models.FloatField(null=True, blank=True)
    optical_state = models.CharField(max_length=20, null=True, blank=True)
    laser_bias_current = models.FloatField(null=True, blank=True)
    tx_operating_current = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Optical Info'
        verbose_name_plural = 'Optical Info'

    def __str__(self):
        return f"Optical: TX {self.tx_power} / RX {self.rx_power}"


class VoIPStatus(BaseModel):
    voip_state = models.CharField(max_length=20, null=True, blank=True)
    sip_server = models.CharField(max_length=255, null=True, blank=True)
    proxy_server = models.CharField(max_length=255, null=True, blank=True)
    registration_state = models.CharField(max_length=50, null=True, blank=True)
    call_duration = models.CharField(max_length=50, null=True, blank=True)
    active_calls = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'VoIP Status'
        verbose_name_plural = 'VoIP Status'

    def __str__(self):
        return f"VoIP: {self.voip_state or 'Unknown'}"