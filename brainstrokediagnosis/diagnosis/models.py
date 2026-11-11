from django.db import models
from django.conf import settings


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Scan(models.Model):
    SCAN_TYPE_CHOICES = [
        ('MRI', 'MRI'),
        ('CT', 'CT Scan'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='scans')
    image = models.ImageField(upload_to='scans/%Y/%m/%d/')
    scan_type = models.CharField(max_length=10, choices=SCAN_TYPE_CHOICES)
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.patient.name} - {self.scan_type} - {self.uploaded_at.strftime('%Y-%m-%d')}"


class Result(models.Model):
    STROKE_TYPE_CHOICES = [
        ('Ischemic', 'Ischemic Stroke'),
        ('Hemorrhagic', 'Hemorrhagic Stroke'),
        ('None', 'No Stroke Detected'),
    ]
    scan = models.OneToOneField(Scan, on_delete=models.CASCADE, related_name='result')
    segmented_image = models.ImageField(upload_to='results/segmented/%Y/%m/%d/', blank=True, null=True)
    stroke_detected = models.BooleanField(default=False)
    stroke_type = models.CharField(max_length=20, choices=STROKE_TYPE_CHOICES, default='None')
    confidence_score = models.FloatField(default=0.0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Detected" if self.stroke_detected else "Not Detected"
        return f"{self.scan.patient.name} - {status}"