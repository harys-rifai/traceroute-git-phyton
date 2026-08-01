from django.db import models

from core.models import BaseModel

TIER_CHOICES = (
    ('TIER_1', 'Tier 1'),
    ('TIER_2', 'Tier 2'),
    ('TIER_3', 'Tier 3'),
    ('TIER_4', 'Tier 4'),
)


class Datacenter(BaseModel):
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name