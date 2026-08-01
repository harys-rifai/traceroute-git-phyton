import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from traceroute.models import WANStatus, WirelessStatus, LANStatus, OpticalStatus, VoIPStatus


class Command(BaseCommand):
    help = 'Seed router status data for demonstration'

    def handle(self, *args, **options):
        self.seed_wan()
        self.seed_wireless()
        self.seed_lan()
        self.seed_optical()
        self.seed_voip()
        self.stdout.write(self.style.SUCCESS('Successfully seeded all router status data'))

    def seed_wan(self):
        WANStatus.objects.all().delete()
        WANStatus.objects.create(
            wan_index=1,
            state='Up',
            mode='TR069_INTERNET',
            ip_type='DHCP',
            ip_address='10.218.56.45',
            subnet_mask='255.255.0.0',
            dns_server='172.17.33.100',
            vlan_id=1490,
            priority=0,
            connection_type='Route',
            wan_mac='88:65:9F:57:26:D9',
            connection_uptime='69 h 37 m 5 s',
            gateway='10.218.0.1',
            ipv6_status='Up',
            ipv6_address='2402:8780:1600::6a:1785',
            ipv6_prefix='2402:8780:106a:1c1c::/64',
            ipv6_gateway='fe80::9225:f2ff:fe18:42ea',
            ipv6_primary_dns='2402:8780:1600::6a:1785',
            ipv6_secondary_dns='2402:8780:1600::6a:1786',
        )
        self.stdout.write('  WAN status seeded')

    def seed_wireless(self):
        WirelessStatus.objects.all().delete()
        WirelessStatus.objects.create(
            ssid='NETWORK-GLOBE',
            bssid='78:8C:B5:E0:D5:35',
            channel=6,
            channel_width='20MHz',
            security_mode='WPA2-PSK',
            signal_strength=85,
            tx_rate=300.0,
            rx_rate=144.0,
            associated_clients=4,
            wifi_state='Enabled',
        )
        self.stdout.write('  Wireless status seeded')

    def seed_lan(self):
        LANStatus.objects.all().delete()
        LANStatus.objects.create(
            lan_ip='192.168.1.1',
            lan_mask='255.255.255.0',
            dhcp_enabled=True,
            dhcp_start='192.168.1.100',
            dhcp_end='192.168.1.200',
            dhcp_lease_time='24h',
            lan_mac='78:8C:B5:E0:D5:35',
            num_clients=4,
        )
        self.stdout.write('  LAN status seeded')

    def seed_optical(self):
        OpticalStatus.objects.all().delete()
        OpticalStatus.objects.create(
            tx_power=3.5,
            rx_power=-12.8,
            tx_bias=15.2,
            temperature=38.5,
            voltage=3.3,
            optical_state='Normal',
            laser_bias_current=12.5,
            tx_operating_current=8.3,
        )
        self.stdout.write('  Optical info seeded')

    def seed_voip(self):
        VoIPStatus.objects.all().delete()
        VoIPStatus.objects.create(
            voip_state='Registered',
            sip_server='sip.example.com',
            proxy_server='proxy.example.com',
            registration_state='Success',
            call_duration='00:00:00',
            active_calls=0,
        )
        self.stdout.write('  VoIP status seeded')