from django.db import models
from core.models import BaseModel
from accounts.models import CustomUser


RECORD_TYPE_CHOICES = (
    ('A', 'A'),
    ('AAAA', 'AAAA'),
    ('MX', 'MX'),
    ('TXT', 'TXT'),
    ('SPF', 'SPF'),
    ('CNAME', 'CNAME'),
    ('NS', 'NS'),
    ('PTR', 'PTR'),
)


class DnsQuery(BaseModel):
    domain = models.CharField(max_length=255)
    record_type = models.CharField(max_length=10, choices=RECORD_TYPE_CHOICES)
    result = models.TextField()
    resolver = models.CharField(max_length=255, null=True, blank=True)
    ttl = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dns_queries'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.domain} ({self.record_type})"
