from django.db import models
from django.conf import settings


class DashboardStats(models.Model):
    date = models.DateField(unique=True)
    total_scans = models.IntegerField(default=0)
    strokes_detected = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.date}"