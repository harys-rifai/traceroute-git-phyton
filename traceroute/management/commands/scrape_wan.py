import time
from datetime import datetime

from django.core.management.base import BaseCommand

from traceroute.tasks import parse_wan_page
import requests
from requests.auth import HTTPBasicAuth


ROUTER_URL = 'http://192.168.1.1/html/main_inter.html'
ROUTER_USER = 'user'
ROUTER_PASS = 'Pro@234!'


class Command(BaseCommand):
    help = 'Scrape WAN status from router at regular intervals'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=5,
            help='Scraping interval in minutes (default: 5)',
        )
        parser.add_argument(
            '--once',
            action='store_true',
            help='Run once and exit instead of continuous loop',
        )

    def handle(self, *args, **options):
        interval = options['interval']
        once = options['once']

        self.stdout.write(self.style.SUCCESS(
            f'[WAN Scraper] Starting — interval: {interval} min'
        ))
        self.stdout.write(f'[WAN Scraper] Router: {ROUTER_URL}')
        if once:
            self.stdout.write('[WAN Scraper] Running once (--once mode)')
        else:
            self.stdout.write('[WAN Scraper] Press Ctrl+C to stop')
            self.stdout.write('-' * 50)

        self.scrape()

        if once:
            self.stdout.write(self.style.SUCCESS('[WAN Scraper] Done.'))
            return

        while True:
            try:
                time.sleep(interval * 60)
                self.scrape()
            except KeyboardInterrupt:
                self.stdout.write('\n[WAN Scraper] Stopped.')
                break

    def scrape(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.stdout.write(f'[{timestamp}] [WAN Scraper] Fetching WAN status...')
        try:
            response = requests.get(
                ROUTER_URL,
                auth=HTTPBasicAuth(ROUTER_USER, ROUTER_PASS),
                timeout=10,
                verify=False,
            )
            response.raise_for_status()
            wan_data = parse_wan_page(response.text)
            self.stdout.write(
                self.style.SUCCESS(
                    f'[{timestamp}] [WAN Scraper] '
                    f'state={wan_data.get("state")}, '
                    f'ip={wan_data.get("ip_address")}, '
                    f'gateway={wan_data.get("gateway")}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'[{timestamp}] [WAN Scraper] Error: {e}')
            )