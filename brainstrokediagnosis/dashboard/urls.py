from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.all_patients, name='patients'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('results/', views.all_results, name='results'),
    path('statistics/', views.statistics, name='statistics'),
]