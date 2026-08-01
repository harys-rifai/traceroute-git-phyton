import os
import sys
import time
import argparse
import requests
from requests.auth import HTTPBasicAuth

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_globe.settings')

import django
django.setup()

from traceroute.tasks import parse_wan_page


ROUTER_URL = 'http://192.168.1.1/html/main_inter.html'
ROUTER_USER = 'user'
ROUTER_PASS = 'Pro@234!'
INTERVAL_SECONDS = 300


def scrape_wan():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] [WAN Scraper] Fetching WAN status...')
    try:
        response = requests.get(
            ROUTER_URL,
            auth=HTTPBasicAuth(ROUTER_USER, ROUTER_PASS),
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        wan_data = parse_wan_page(response.text)
        print(f'[{timestamp}] [WAN Scraper] state={wan_data.get("state")}, ip={wan_data.get("ip_address")}')
    except Exception as e:
        print(f'[{timestamp}] [WAN Scraper] Error: {e}')


def run_scheduler():
    print(f'[WAN Scraper] Scheduler started — interval: {INTERVAL_SECONDS // 60} min')
    print(f'[WAN Scraper] Router: {ROUTER_URL}')
    print(f'[WAN Scraper] Press Ctrl+C to stop')
    print('-' * 50)

    scrape_wan()

    while True:
        time.sleep(INTERVAL_SECONDS)
        scrape_wan()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WAN Status Scraper')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--interval', type=int, default=5, help='Scraping interval in minutes')
    args = parser.parse_args()

    INTERVAL_SECONDS = args.interval * 60

    try:
        if args.once:
            scrape_wan()
        else:
            run_scheduler()
    except KeyboardInterrupt:
        print('\n[WAN Scraper] Scheduler stopped.')