from django.contrib import admin


class CustomAdminSite(admin.AdminSite):
    site_header = "Network Globe Scanner Administration"
    site_title = "Network Globe Admin"
    index_title = "Dashboard Overview"
    index_template = 'admin/dashboard.html'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.dashboard_view), name='index'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        from traceroute.models import Traceroute
        from datacenter.models import Datacenter
        from servers.models import Server
        from dnslookup.models import DnsQuery
        from django.shortcuts import render

        context = {
            **self.each_context(request),
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


admin_site = CustomAdminSite(name='admin')
