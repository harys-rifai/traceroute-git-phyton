from django.db import models

from core.models import BaseModel
from datacenter.models import Datacenter


STATUS_CHOICES = (
    ('ONLINE', 'Online'),
    ('OFFLINE', 'Offline'),
    ('MAINTENANCE', 'Maintenance'),
)


class Server(BaseModel):
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    datacenter = models.ForeignKey(
        Datacenter,
        on_delete=models.CASCADE,
        related_name='servers',
    )
    os = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.hostname} ({self.ip_address})"
