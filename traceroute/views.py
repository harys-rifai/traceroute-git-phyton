from collections import defaultdict

from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Traceroute, TracerouteHop, WANStatus
from .serializers import TracerouteSerializer, TracerouteHopSerializer
from .tasks import run_traceroute


class TracerouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Traceroute.objects.all()
    serializer_class = TracerouteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        run_traceroute.delay(serializer.instance.id)


class TracerouteResultViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Traceroute.objects.all()
    serializer_class = TracerouteSerializer
    permission_classes = [IsAuthenticated]


def traceroute_result(request, target):
    traceroute = get_object_or_404(Traceroute, target=target)
    hops = traceroute.hops.all()
    total_hops = hops.count()
    mapped_hops = hops.exclude(loss=100).count()
    dest_hop = hops.last()
    dest_rtt = dest_hop.latency if dest_hop and dest_hop.latency else 0
    avg_latency = hops.aggregate(avg=Avg('latency'))['avg']
    avg_response = round(avg_latency, 2) if avg_latency else 0

    networks = []
    as_groups = defaultdict(list)
    for hop in hops:
        if hop.asn:
            as_groups[hop.asn].append(hop)

    for asn, group_hops in as_groups.items():
        first = group_hops[0]
        latencies = [h.latency for h in group_hops if h.latency is not None]
        avg_lat = round(sum(latencies) / len(latencies), 2) if latencies else 0
        networks.append({
            'as_name': first.hostname or asn,
            'asn': asn,
            'avg_response': avg_lat,
            'hosts': len(group_hops),
        })

    return render(request, 'traceroute/result.html', {
        'traceroute': traceroute,
        'hops': hops,
        'total_hops': total_hops,
        'mapped_hops': mapped_hops,
        'dest_rtt': dest_rtt,
        'avg_response': avg_response,
        'networks': networks,
    })


def wan_status(request):
    wan_entries = WANStatus.objects.all()[:10]
    latest_wan = WANStatus.objects.first()
    return render(request, 'traceroute/wan_status.html', {
        'wan_entries': wan_entries,
        'latest_wan': latest_wan,
    })


def wan_status_api(request):
    from django.http import JsonResponse
    latest = WANStatus.objects.first()
    if not latest:
        return JsonResponse({'error': 'No WAN data available'}, status=404)
    data = {
        'wan_index': latest.wan_index,
        'state': latest.state,
        'mode': latest.mode,
        'ip_type': latest.ip_type,
        'ip_address': latest.ip_address,
        'subnet_mask': latest.subnet_mask,
        'dns_server': latest.dns_server,
        'vlan_id': latest.vlan_id,
        'priority': latest.priority,
        'connection_type': latest.connection_type,
        'wan_mac': latest.wan_mac,
        'connection_uptime': latest.connection_uptime,
        'gateway': latest.gateway,
        'ipv6_status': latest.ipv6_status,
        'ipv6_address': latest.ipv6_address,
        'ipv6_prefix': latest.ipv6_prefix,
        'ipv6_gateway': latest.ipv6_gateway,
        'ipv6_primary_dns': latest.ipv6_primary_dns,
        'ipv6_secondary_dns': latest.ipv6_secondary_dns,
        'created_at': latest.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return JsonResponse(data)