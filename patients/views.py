from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from doctor.models import *
from patients.models import *
from patients.forms import ReportForm
from user.deco import allowedUsers
from datetime import date, datetime
from django.utils import timezone
import os


User = get_user_model()

# Create your views here.
@login_required
@allowedUsers(['PAT'])
def PatDash(request):
    return render(request, "pat/pat_dash.html")

@login_required
@allowedUsers(['PAT'])
def ExploreDoctors(request):
    """View for patients to explore and connect with doctors"""
    # Get all doctors with their profiles
    doctors = DoctorProfile.objects.select_related("user").all()

    # Get search parameters
    specialization = request.GET.get("specialization", "")
    search_query = request.GET.get("search", "")

    # Filter doctors based on search criteria
    if specialization:
        doctors = doctors.filter(specialization=specialization)

    if search_query:
        doctors = (
            doctors.filter(user__first_name__icontains=search_query)
            | doctors.filter(user__last_name__icontains=search_query)
            | doctors.filter(specialization__icontains=search_query)
        )

    # Get connection status for each doctor
    patient = request.user.PAT
    for doctor in doctors:
        try:
            request_obj = PatientConnectionRequest.objects.get(patient=patient, doctor=doctor)
            doctor.connection_status = request_obj.request_status
            doctor.connection_request_id = request_obj.id
        except PatientConnectionRequest.DoesNotExist:
            doctor.connection_status = None
            doctor.connection_request_id = None

    # Get all specialization choices for filter dropdown
    specialization_choices = DoctorProfile.SPECIALIZATION_CHOICES

    context = {
        "doctors": doctors,
        "specialization_choices": specialization_choices,
        "current_specialization": specialization,
        "search_query": search_query,
    }

    return render(request, "pat/pat_explore.html", context)


@login_required
@allowedUsers(['PAT'])
def PatMedication(request):
    pat = request.user.PAT
    active_medications = Medication.objects.filter(patient = pat,status="ACTIVE")
    discontinued_medications = Medication.objects.filter(patient = pat,status="DISCONTINUED")

    context = {
        "active_medications": active_medications,
        "discontinued_medications": discontinued_medications,
    }
    return render(request, "pat/pat_medication.html", context)


@login_required
@require_POST
@allowedUsers(['PAT'])
def SendConnectionRequest(request):
    """Handle sending connection requests to doctors"""
    doctor_id = request.POST.get("doctor_id")
    note = request.POST.get("note")

    if not doctor_id:
        return JsonResponse({"success": False, "message": "Doctor ID is required"})

    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
        patient = request.user.PAT  # Get the patient's PatientRecord

        # Create a PatientRequest object
        patient_request = PatientConnectionRequest.objects.create(
            patient=patient,
            doctor=doctor,
            notes=note or "",  # Use empty string if note is None
        )

        return JsonResponse(
            {
                "success": True,
                "message": f"Connection request sent to {doctor.full_name}",
            }
        )
    except DoctorProfile.DoesNotExist:
        return JsonResponse({"success": False, "message": "Doctor not found"})
    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Error creating request: {str(e)}"}
        )


@login_required
@allowedUsers(['PAT'])
def PatReports(request):
    """View for patients to manage their reports"""
    patient = request.user.PAT
    reports = Report.objects.filter(patient=patient)

    # Filter by report type if provided
    report_type = request.GET.get('report_type', '')
    if report_type:
        reports = reports.filter(report_type=report_type)

    # Filter by uploaded by if provided
    uploaded_by = request.GET.get('uploaded_by', '')
    if uploaded_by:
        reports = reports.filter(uploaded_by__first_name__icontains=uploaded_by)

    # Search by title
    search_query = request.GET.get('search', '')
    if search_query:
        reports = reports.filter(title__icontains=search_query)

    # Get unique uploaders for filter dropdown
    uploaders = User.objects.filter(uploaded_reports__patient=patient).distinct()

    context = {
        'reports': reports,
        'report_types': Report.REPORT_TYPE_CHOICES,
        'uploaders': uploaders,
        'current_report_type': report_type,
        'current_uploaded_by': uploaded_by,
        'search_query': search_query,
    }
    return render(request, "pat/pat_reports.html", context)


@login_required
@allowedUsers(['PAT'])
def AddReport(request):
    """View for patients to add new reports"""
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = request.user.PAT
            report.uploaded_by = request.user
            report.save()
            messages.success(request, 'Report uploaded successfully!')
            return redirect('PAT_REPORTS')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReportForm()

    context = {
        'form': form,
        'action': 'Add'
    }
    return render(request, "pat/pat_add_edit_report.html", context)


@login_required
@allowedUsers(['PAT'])
def EditReport(request, report_id):
    """View for patients to edit their reports"""
    report = get_object_or_404(Report, id=report_id, patient=request.user.PAT)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully!')
            return redirect('PAT_REPORTS')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReportForm(instance=report)

    context = {
        'form': form,
        'report': report,
        'action': 'Edit'
    }
    return render(request, "pat/pat_add_edit_report.html", context)


@login_required
@allowedUsers(['PAT'])
def ViewReport(request, report_id):
    """View for patients to view a specific report"""
    report = get_object_or_404(Report, id=report_id, patient=request.user.PAT)

    context = {
        'report': report
    }
    return render(request, "pat/pat_view_report.html", context)


@login_required
@allowedUsers(['PAT'])
def DeleteReport(request, report_id):
    """View for patients to delete their reports"""
    report = get_object_or_404(Report, id=report_id, patient=request.user.PAT)

    if request.method == 'POST':
        # Delete the file from storage
        if report.file:
            if os.path.exists(report.file.path):
                os.remove(report.file.path)

        report.delete()
        messages.success(request, 'Report deleted successfully!')
        return redirect('PAT_REPORTS')

    context = {
        'report': report
    }
    return render(request, "pat/pat_delete_report.html", context)


@login_required
@allowedUsers(['PAT'])
def DownloadReport(request, report_id):
    """View for patients to download their report files"""
    report = get_object_or_404(Report, id=report_id, patient=request.user.PAT)

    if report.file:
        response = HttpResponse(report.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(report.file.name)}"'
        return response
    else:
        messages.error(request, 'File not found.')
        return redirect('PAT_REPORTS')



@login_required
def patient_appointments(request):
    scheduled = Appointment.objects.filter(
        patient=request.user.PAT, status="scheduled"
    ).order_by("-date_time")
    completed = Appointment.objects.filter(
        patient=request.user.PAT, status="completed"
    ).order_by("-date_time")
    cancelled = Appointment.objects.filter(
        patient=request.user.PAT, status="cancelled"
    ).order_by("-date_time")
    now = timezone.now()
    context = {
        "scheduled": scheduled,
        "completed": completed,
        "cancelled": cancelled,
        "now": now,
    }
    return render(request, 'pat/patient_appointments.html', context)
