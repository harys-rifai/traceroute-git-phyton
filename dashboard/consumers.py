import json
import random

from channels.generic.websocket import WebsocketConsumer


class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def send_stats(self):
        stats = {
            'total_scans': random.randint(1000, 5000),
            'active_servers': random.randint(50, 200),
            'global_datacenters': random.randint(10, 50),
            'dns_queries': random.randint(5000, 20000),
            'average_latency': round(random.uniform(20, 100), 2),
            'packet_loss': round(random.uniform(0, 5), 2),
        }
        self.send(text_data=json.dumps(stats))

    def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('action') == 'start_streaming':
            import asyncio
            from channels.db import database_sync_to_async

            async def stream():
                while True:
                    self.send_stats()
                    await asyncio.sleep(5)

            asyncio.get_event_loop().run_until_complete(stream())


class TracerouteConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        traceroute_id = data.get('traceroute_id')

        if traceroute_id:
            for progress in range(0, 101, 20):
                update = {
                    'traceroute_id': traceroute_id,
                    'progress': progress,
                    'status': 'in_progress' if progress < 100 else 'completed',
                    'hops': progress // 10,
                }
                self.send(text_data=json.dumps(update))
