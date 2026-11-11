from django.contrib import admin
from .models import DashboardStats


@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_scans', 'strokes_detected']
    list_filter = ['date']
    date_hierarchy = 'date'