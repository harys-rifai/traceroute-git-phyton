from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from traceroute.models import Traceroute, WANStatus, WirelessStatus, LANStatus, OpticalStatus, VoIPStatus
from traceroute.serializers import TracerouteHopSerializer
from servers.models import Server
from datacenter.models import Datacenter
from dnslookup.models import DnsQuery


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'


class AnimationsView(TemplateView):
    template_name = 'dashboard/animations.html'


class DashboardStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total_scans = Traceroute.objects.count()
        active_servers = Server.objects.filter(status='ONLINE').count()
        global_datacenters = Datacenter.objects.count()
        dns_queries = DnsQuery.objects.count()
        average_latency = round(45 + (total_scans % 20), 2)
        packet_loss = round((active_servers % 10) * 0.5, 2)

        latest_wan = WANStatus.objects.first()
        latest_wireless = WirelessStatus.objects.first()
        latest_lan = LANStatus.objects.first()
        latest_optical = OpticalStatus.objects.first()
        latest_voip = VoIPStatus.objects.first()

        return Response({
            'total_scans': total_scans,
            'active_servers': active_servers,
            'global_datacenters': global_datacenters,
            'dns_queries': dns_queries,
            'average_latency': average_latency,
            'packet_loss': packet_loss,
            'wan_ip': latest_wan.ip_address if latest_wan else None,
            'wan_state': latest_wan.state if latest_wan else None,
            'wan_gateway': latest_wan.gateway if latest_wan else None,
            'wan_uptime': latest_wan.connection_uptime if latest_wan else None,
            'wan_mac': latest_wan.wan_mac if latest_wan else None,
            'wan_type': latest_wan.connection_type if latest_wan else None,
            'wan_ipv6_status': latest_wan.ipv6_status if latest_wan else None,
            'wan_ipv6_address': latest_wan.ipv6_address if latest_wan else None,
            'wireless_ssid': latest_wireless.ssid if latest_wireless else None,
            'wireless_state': latest_wireless.wifi_state if latest_wireless else None,
            'wireless_signal': latest_wireless.signal_strength if latest_wireless else None,
            'wireless_clients': latest_wireless.associated_clients if latest_wireless else None,
            'lan_ip': latest_lan.lan_ip if latest_lan else None,
            'lan_clients': latest_lan.num_clients if latest_lan else None,
            'optical_state': latest_optical.optical_state if latest_optical else None,
            'voip_state': latest_voip.voip_state if latest_voip else None,
        })


class UnifiedDashboardView(TemplateView):
    template_name = 'dashboard/unified.html'


class UnifiedDashboardStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total_scans = Traceroute.objects.count()
        active_servers = Server.objects.filter(status='ONLINE').count()
        global_datacenters = Datacenter.objects.count()
        dns_queries = DnsQuery.objects.count()
        average_latency = round(45 + (total_scans % 20), 2)
        packet_loss = round((active_servers % 10) * 0.5, 2)

        latest_wan = WANStatus.objects.first()
        wan_data = None
        if latest_wan:
            wan_data = {
                'wan_index': latest_wan.wan_index,
                'state': latest_wan.state,
                'ip_address': latest_wan.ip_address,
                'gateway': latest_wan.gateway,
                'connection_type': latest_wan.connection_type,
                'wan_mac': latest_wan.wan_mac,
                'connection_uptime': latest_wan.connection_uptime,
                'ipv6_status': latest_wan.ipv6_status,
                'ipv6_address': latest_wan.ipv6_address,
            }

        latest_wireless = WirelessStatus.objects.first()
        wireless_data = None
        if latest_wireless:
            wireless_data = {
                'ssid': latest_wireless.ssid,
                'wifi_state': latest_wireless.wifi_state,
                'signal_strength': latest_wireless.signal_strength,
                'associated_clients': latest_wireless.associated_clients,
            }

        latest_lan = LANStatus.objects.first()
        lan_data = None
        if latest_lan:
            lan_data = {
                'lan_ip': latest_lan.lan_ip,
                'num_clients': latest_lan.num_clients,
            }

        latest_optical = OpticalStatus.objects.first()
        optical_data = None
        if latest_optical:
            optical_data = {
                'optical_state': latest_optical.optical_state,
                'tx_power': latest_optical.tx_power,
                'rx_power': latest_optical.rx_power,
            }

        latest_voip = VoIPStatus.objects.first()
        voip_data = None
        if latest_voip:
            voip_data = {
                'voip_state': latest_voip.voip_state,
                'registration_state': latest_voip.registration_state,
            }

        return Response({
            'total_scans': total_scans,
            'active_servers': active_servers,
            'global_datacenters': global_datacenters,
            'dns_queries': dns_queries,
            'average_latency': average_latency,
            'packet_loss': packet_loss,
            'wan_status': wan_data,
            'wireless_status': wireless_data,
            'lan_status': lan_data,
            'optical_status': optical_data,
            'voip_status': voip_data,
        })
