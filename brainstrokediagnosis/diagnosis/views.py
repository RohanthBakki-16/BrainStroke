from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
import os
import numpy as np
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Patient, Scan, Result
from .ml_model.predict import predict_stroke, load_model


@login_required
def upload_scan(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        patient_age = request.POST.get('patient_age')
        patient_gender = request.POST.get('patient_gender')
        patient_phone = request.POST.get('patient_phone')
        patient_email = request.POST.get('patient_email')
        
        scan_type = request.POST.get('scan_type')
        scan_image = request.FILES.get('scan_image')
        notes = request.POST.get('notes')

        if not scan_image:
            messages.error(request, 'Please upload a scan image!')
            return redirect('upload_scan')

        patient, created = Patient.objects.get_or_create(
            name=patient_name,
            defaults={
                'age': patient_age,
                'gender': patient_gender,
                'phone': patient_phone,
                'email': patient_email
            }
        )

        if not created:
            patient.age = patient_age
            patient.gender = patient_gender
            patient.phone = patient_phone
            patient.email = patient_email
            patient.save()

        scan = Scan.objects.create(
            patient=patient,
            image=scan_image,
            scan_type=scan_type,
            notes=notes,
            uploaded_by=request.user
        )

        try:
            image_path = scan.image.path
            load_model()
            prediction = predict_stroke(image_path, scan_type)

            if prediction['segmented_image'] is not None:
                segmented_array = prediction['segmented_image']
                segmented_image = array_to_image(segmented_array, scan_image.name)
            else:
                segmented_image = None

            result = Result.objects.create(
                scan=scan,
                segmented_image=segmented_image,
                stroke_detected=prediction['stroke_detected'],
                stroke_type=prediction['stroke_type'],
                confidence_score=prediction['confidence_score']
            )

            messages.success(request, f'Prediction complete: {prediction["stroke_type"]} ({prediction["confidence_score"]}%)')
            return redirect('result_detail', result_id=result.id)

        except Exception as e:
            messages.error(request, f'Error processing image: {str(e)}')
            return redirect('upload_scan')

    return render(request, 'diagnosis/upload.html')


@login_required
def result_detail(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    return render(request, 'diagnosis/result_detail.html', {'result': result})


@login_required
def scan_list(request):
    scans = Scan.objects.all().order_by('-uploaded_at')
    paginator = Paginator(scans, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'diagnosis/scan_list.html', {'page_obj': page_obj})


@login_required
def patient_scans(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    scans = Scan.objects.filter(patient=patient).order_by('-uploaded_at')
    return render(request, 'diagnosis/patient_scans.html', {'patient': patient, 'scans': scans})


def array_to_image(array, original_filename):
    """Convert numpy array to Django ImageField."""
    array = np.clip(array, 0, 255).astype(np.uint8)
    image = Image.fromarray(array)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    filename = f"segmented_{os.path.splitext(original_filename)[0]}.png"
    return InMemoryUploadedFile(
        buffer, None, filename, 'image/png', buffer.tell(), None
    )