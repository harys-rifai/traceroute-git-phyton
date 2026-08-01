import random
import re
import requests
from requests.auth import HTTPBasicAuth

from network_globe.celery import app as celery_app
from .models import Traceroute, TracerouteHop, WANStatus


@celery_app.task(bind=True, name='traceroute.run_traceroute')
def run_traceroute(self, traceroute_id):
    try:
        traceroute = Traceroute.objects.get(id=traceroute_id)
        traceroute.status = 'RUNNING'
        traceroute.save()

        num_hops = random.randint(3, 5)
        for i in range(1, num_hops + 1):
            TracerouteHop.objects.create(
                traceroute=traceroute,
                hop_number=i,
                ip_address=f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}",
                hostname=f"hop-{i}.example.com",
                latency=round(random.uniform(1, 200), 2),
                country="US",
                city="New York",
                asn=f"AS{random.randint(1000, 99999)}",
            )

        traceroute.status = 'COMPLETED'
        traceroute.save()
    except Exception as e:
        traceroute.status = 'FAILED'
        traceroute.save()
        raise


@celery_app.task(name='traceroute.run_dns_query')
def run_dns_query(traceroute_id, domain):
    return {
        'domain': domain,
        'traceroute_id': traceroute_id,
        'results': [
            {'type': 'A', 'value': f"192.168.1.{random.randint(1, 254)}"},
            {'type': 'NS', 'value': f"ns1.{domain}"},
            {'type': 'MX', 'value': f"mail.{domain}"},
        ],
    }


@celery_app.task(name='traceroute.fetch_wan_status')
def fetch_wan_status():
    router_url = 'http://192.168.1.1/html/main_inter.html'
    username = 'user'
    password = 'Pro@234!'

    try:
        response = requests.get(
            router_url,
            auth=HTTPBasicAuth(username, password),
            timeout=10,
            verify=False,
        )
        response.raise_for_status()

        wan_data = parse_wan_page(response.text)

        WANStatus.objects.update_or_create(
            wan_index=wan_data.get('wan_index', 1),
            defaults=wan_data,
        )

        return wan_data
    except Exception as e:
        return {'error': str(e)}


@celery_app.task(name='traceroute.fetch_device_info')
def fetch_device_info():
    router_url = 'http://192.168.1.1/html/main_inter.html'
    username = 'user'
    password = 'Pro@234!'

    try:
        response = requests.get(
            router_url,
            auth=HTTPBasicAuth(username, password),
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return parse_device_info(response.text)
    except Exception as e:
        return {'error': str(e)}


def parse_wan_page(html):
    wan_data = {
        'wan_index': 1,
        'state': 'Unknown',
        'mode': None,
        'ip_type': None,
        'ip_address': None,
        'subnet_mask': None,
        'dns_server': None,
        'vlan_id': None,
        'priority': None,
        'connection_type': None,
        'wan_mac': None,
        'connection_uptime': None,
        'gateway': None,
        'ipv6_status': None,
        'ipv6_address': None,
        'ipv6_prefix': None,
        'ipv6_gateway': None,
        'ipv6_primary_dns': None,
        'ipv6_secondary_dns': None,
    }

    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)

    state_match = re.search(r'\b(Up|Down|Idle)\b', text, re.IGNORECASE)
    if state_match:
        wan_data['state'] = state_match.group(1)

    mode_match = re.search(r'\b(TR069_INTERNET|PPPOE|DHCP|STATIC)\b', text, re.IGNORECASE)
    if mode_match:
        wan_data['mode'] = mode_match.group(1)

    ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text)
    if ip_match:
        wan_data['ip_address'] = ip_match.group(1)

    mask_match = re.search(r'Mask[:\s]*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text, re.IGNORECASE)
    if mask_match:
        wan_data['subnet_mask'] = mask_match.group(1)

    dns_match = re.search(r'DNS[:\s]*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text, re.IGNORECASE)
    if dns_match:
        wan_data['dns_server'] = dns_match.group(1)

    gw_match = re.search(r'Gateway[:\s]*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text, re.IGNORECASE)
    if gw_match:
        wan_data['gateway'] = gw_match.group(1)

    mac_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', text)
    if mac_match:
        wan_data['wan_mac'] = mac_match.group(0).upper()

    uptime_match = re.search(r'Uptime[:\s]*([\d\s\w]+)', text, re.IGNORECASE)
    if uptime_match:
        wan_data['connection_uptime'] = uptime_match.group(1).strip()

    ipv6_match = re.search(r'(2402:[0-9a-fA-F:]+)', text)
    if ipv6_match:
        wan_data['ipv6_address'] = ipv6_match.group(1)

    prefix_match = re.search(r'([0-9a-fA-F]{4}:){2,7}[0-9a-fA-F]{0,4}/\d{1,3}', text)
    if prefix_match:
        wan_data['ipv6_prefix'] = prefix_match.group(0)

    ipv6_gw_match = re.search(r'fe80::[0-9a-fA-F:]+', text)
    if ipv6_gw_match:
        wan_data['ipv6_gateway'] = ipv6_gw_match.group(0)

    return wan_data


def parse_device_info(html):
    device_info = {
        'device_name': None,
        'model': None,
        'firmware_version': None,
        'hardware_version': None,
        'serial_number': None,
        'uptime': None,
        'cpu_usage': None,
        'memory_usage': None,
    }

    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)

    name_match = re.search(r'Device Name[:\s]*([\w\s\-]+)', text, re.IGNORECASE)
    if name_match:
        device_info['device_name'] = name_match.group(1).strip()

    model_match = re.search(r'Model[:\s]*([\w\s\-]+)', text, re.IGNORECASE)
    if model_match:
        device_info['model'] = model_match.group(1).strip()

    fw_match = re.search(r'Firmware[:\s]*([\d\.]+)', text, re.IGNORECASE)
    if fw_match:
        device_info['firmware_version'] = fw_match.group(1).strip()

    hw_match = re.search(r'Hardware[:\s]*([\d\.]+)', text, re.IGNORECASE)
    if hw_match:
        device_info['hardware_version'] = hw_match.group(1).strip()

    serial_match = re.search(r'Serial[:\s]*([\w\-]+)', text, re.IGNORECASE)
    if serial_match:
        device_info['serial_number'] = serial_match.group(1).strip()

    uptime_match = re.search(r'Uptime[:\s]*([\d\s\w]+)', text, re.IGNORECASE)
    if uptime_match:
        device_info['uptime'] = uptime_match.group(1).strip()

    cpu_match = re.search(r'CPU[:\s]*([\d\.]+)%', text, re.IGNORECASE)
    if cpu_match:
        device_info['cpu_usage'] = cpu_match.group(1)

    mem_match = re.search(r'Memory[:\s]*([\d\.]+)%', text, re.IGNORECASE)
    if mem_match:
        device_info['memory_usage'] = mem_match.group(1)

    return device_info