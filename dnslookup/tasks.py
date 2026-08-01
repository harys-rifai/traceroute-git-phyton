from network_globe.celery import celery_app


@celery_app.task(bind=True, name='dnslookup.run_dns_query')
def run_dns_query(self, domain, record_type):
    mock_results = {
        'A': ['93.184.216.34'],
        'AAAA': ['2606:2800:220:1:248:1893:25c8:1946'],
        'MX': ['10 mail.example.com'],
        'TXT': ['v=spf1 include:_spf.google.com ~all'],
        'SPF': ['v=spf1 include:_spf.google.com ~all'],
        'CNAME': ['alias.example.com'],
        'NS': ['ns1.example.com', 'ns2.example.com'],
        'PTR': ['host.example.com'],
    }
    result = {
        'domain': domain,
        'record_type': record_type,
        'records': mock_results.get(record_type, []),
    }
    return result
