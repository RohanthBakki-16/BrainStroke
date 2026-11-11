from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_scan, name='upload_scan'),
    path('result/<int:result_id>/', views.result_detail, name='result_detail'),
    path('scans/', views.scan_list, name='scan_list'),
    path('patient/<int:patient_id>/scans/', views.patient_scans, name='patient_scans'),
]