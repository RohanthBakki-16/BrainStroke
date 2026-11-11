from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg
from django.core.paginator import Paginator
from datetime import datetime, timedelta

from diagnosis.models import Patient, Scan, Result


@login_required
def dashboard(request):
    total_scans = Scan.objects.count()
    total_patients = Patient.objects.count()
    strokes_detected = Result.objects.filter(stroke_detected=True).count()
    recent_results = Result.objects.select_related('scan__patient').order_by('-created_at')[:5]
    
    ischemic_count = Result.objects.filter(stroke_type='Ischemic').count()
    hemorrhagic_count = Result.objects.filter(stroke_type='Hemorrhagic').count()
    
    scans_today = Scan.objects.filter(uploaded_at__date=datetime.now().date()).count()
    
    context = {
        'total_scans': total_scans,
        'total_patients': total_patients,
        'strokes_detected': strokes_detected,
        'recent_results': recent_results,
        'ischemic_count': ischemic_count,
        'hemorrhagic_count': hemorrhagic_count,
        'scans_today': scans_today,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def all_patients(request):
    patients = Patient.objects.all().order_by('-created_at')
    paginator = Paginator(patients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/patients.html', {'page_obj': page_obj})


@login_required
def patient_detail(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    scans = Scan.objects.filter(patient=patient).order_by('-uploaded_at')
    return render(request, 'dashboard/patient_detail.html', {'patient': patient, 'scans': scans})


@login_required
def all_results(request):
    results = Result.objects.select_related('scan__patient').order_by('-created_at')
    
    filter_type = request.GET.get('filter')
    if filter_type == 'stroke':
        results = results.filter(stroke_detected=True)
    elif filter_type == 'no_stroke':
        results = results.filter(stroke_detected=False)
    elif filter_type == 'ischemic':
        results = results.filter(stroke_type='Ischemic')
    elif filter_type == 'hemorrhagic':
        results = results.filter(stroke_type='Hemorrhagic')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        results = results.filter(created_at__date__gte=start_date)
    if end_date:
        results = results.filter(created_at__date__lte=end_date)
    
    paginator = Paginator(results, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/results.html', {'page_obj': page_obj, 'filter_type': filter_type})


@login_required
def statistics(request):
    total_scans = Scan.objects.count()
    total_patients = Patient.objects.count()
    strokes_detected = Result.objects.filter(stroke_detected=True).count()
    no_stroke = Result.objects.filter(stroke_detected=False).count()
    
    ischemic = Result.objects.filter(stroke_type='Ischemic').count()
    hemorrhagic = Result.objects.filter(stroke_type='Hemorrhagic').count()
    
    last_30_days = datetime.now() - timedelta(days=30)
    recent_scans = Scan.objects.filter(uploaded_at__gte=last_30_days).count()
    
    avg_confidence = Result.objects.aggregate(avg=Avg('confidence_score'))['avg'] or 0
    
    context = {
        'total_scans': total_scans,
        'total_patients': total_patients,
        'strokes_detected': strokes_detected,
        'no_stroke': no_stroke,
        'ischemic': ischemic,
        'hemorrhagic': hemorrhagic,
        'recent_scans': recent_scans,
        'avg_confidence': round(avg_confidence, 2),
    }
    return render(request, 'dashboard/statistics.html', context)