from django.contrib import admin
from django.db.models import Count
from django.shortcuts import render

from traceroute.models import Traceroute
from datacenter.models import Datacenter
from servers.models import Server
from dnslookup.models import DnsQuery


def dashboard_view(request):
    context = {
        'total_traceroutes': Traceroute.objects.count(),
        'total_datacenters': Datacenter.objects.count(),
        'total_servers': Server.objects.count(),
        'total_dns_queries': DnsQuery.objects.count(),
        'datacenters': Datacenter.objects.all()[:10],
        'servers': Server.objects.select_related('datacenter')[:10],
        'traceroutes': Traceroute.objects.all()[:10],
        'dns_queries': DnsQuery.objects.all()[:10],
        'title': 'Dashboard Overview',
    }
    return render(request, 'admin/dashboard.html', context)

# Override default admin index template
admin.site.index_template = 'admin/dashboard.html'
