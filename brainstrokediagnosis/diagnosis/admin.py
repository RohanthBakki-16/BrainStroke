from django.contrib import admin
from .models import Patient, Scan, Result


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['gender', 'created_at']


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ['patient', 'scan_type', 'uploaded_at', 'uploaded_by']
    list_filter = ['scan_type', 'uploaded_at']
    search_fields = ['patient__name', 'notes']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['scan', 'stroke_detected', 'stroke_type', 'confidence_score', 'created_at']
    list_filter = ['stroke_detected', 'stroke_type', 'created_at']
    search_fields = ['scan__patient__name']