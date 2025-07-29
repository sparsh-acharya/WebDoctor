from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When
from doctor.forms import AppointmentForm, MedicationForm, EditVitalsForm
from doctor.models import *
from user.deco import allowedUsers
from patients.models import *
from patients.forms import ReportForm
from django.db import models
import os
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


# Create your views here.
@login_required
@allowedUsers(["DOC"])
def DocDash(request):
    search_query = request.GET.get("search", "")
    doc = request.user.DOC
    patientslist = PatientsList.objects.filter(doctor=doc).select_related(
        "patient__user"
    )
    if search_query:
        patientslist = patientslist.filter(
            Q(patient__user__first_name__icontains=search_query)
            | Q(patient__user__last_name__icontains=search_query)
            | Q(patient__user__phone_number__icontains=search_query)
            | Q(patient__user__gender__icontains=search_query)
            | Q(patient__blood_type__icontains=search_query)
        )
    patients = [pl.patient for pl in patientslist]

    # Fetch today's appointments in local timezone
    now = timezone.localtime(timezone.now())
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    todays_appointments = Appointment.objects.filter(
        doctor=doc,
        date_time__gte=start_of_day,
        date_time__lte=end_of_day,
        status="scheduled"
    ).select_related("patient__user").order_by("date_time")

    context = {
        "patients": patients,
        "search_query": search_query,
        "todays_appointments": todays_appointments,
        "now":now,
    }
    return render(request, "doc/doc_dash.html", context)


@login_required
@allowedUsers(["DOC"])
def DocReq(request):
    doc = request.user.DOC  # or the correct related_name if different
    pending_requests = PatientConnectionRequest.objects.filter(
        doctor=doc, request_status="PENDING"
    )
    return render(request, "doc/doc_requests.html", {"requests": pending_requests})


@login_required
@require_POST
@allowedUsers(["DOC"])
def approve_request(request, request_id):
    req = get_object_or_404(PatientConnectionRequest, id=request_id)
    req.request_status = "APPROVED"
    req.save()
    pat = req.patient
    doc = req.doctor
    try:
        patientList = PatientsList.objects.create(patient=pat, doctor=doc)
        return JsonResponse(
            {"success": True, "message": f"connected to patien {pat.full_name}"}
        )
    except Exception as e:
        return JsonResponse(
            {
                "success": False,
                "message": f"Error adding patient to your list: {str(e)}",
            }
        )


@login_required
@allowedUsers(["DOC"])
def reject_request(request, request_id):
    req = get_object_or_404(PatientConnectionRequest, id=request_id)
    req.delete()

    return redirect("DOC_REQ")


@login_required
@allowedUsers(["DOC"])
def DocPats(request):
    doc = request.user.DOC
    search_query = request.GET.get("search", "")
    patientslist = PatientsList.objects.filter(doctor=doc)
    if search_query:
        patientslist = patientslist.filter(
            Q(patient__user__first_name__icontains=search_query)
            | Q(patient__user__last_name__icontains=search_query)
            | Q(patient__user__phone_number__icontains=search_query)
            | Q(patient__user__gender__icontains=search_query)
            | Q(patient__blood_type__icontains=search_query)
        )
    context = {"list": patientslist, "search_query": search_query}
    return render(request, "doc/doc_my_patients.html", context)


@login_required
@allowedUsers(["DOC"])
def patient_detail(request, patient_id):
    # Ensure the patient exists and is linked to the current doctor
    patient_list_entry = get_object_or_404(
        PatientsList, patient__id=patient_id, doctor=request.user.DOC
    )
    patient = patient_list_entry.patient

    # --- Medication Filtering/Search ---
    med_search = request.GET.get("med_search", "").strip()
    med_status = request.GET.get("med_status", "")
    medications = Medication.objects.filter(patient=patient, doctor=request.user.DOC)
    if med_search:
        medications = medications.filter(
            Q(name__icontains=med_search)
            | Q(dosage__icontains=med_search)
            | Q(frequency__icontains=med_search)
            | Q(start_date__icontains=med_search)
            | Q(duration__icontains=med_search)
            | Q(status__icontains=med_search)
        )
    if med_status:
        medications = medications.filter(status=med_status)
    medications = medications.order_by(
        Case(
            When(status="ACTIVE", then=0),
            default=1,
            output_field=models.IntegerField(),
        ),
        "start_date",
    )

    # --- Report Filtering/Search ---
    report_search = request.GET.get("report_search", "").strip()
    report_type = request.GET.get("report_type", "")
    reports = Report.objects.filter(patient=patient)
    if report_search:
        reports = reports.filter(
            Q(title__icontains=report_search)
            | Q(report_type__icontains=report_search)
            | Q(report_date__icontains=report_search)
            | Q(description__icontains=report_search)
            | Q(lab_facility__icontains=report_search)
        )
    if report_type:
        reports = reports.filter(report_type=report_type)
    reports = reports.order_by("-report_date", "-uploaded_date")

    report_form = ReportForm()
    med_form = MedicationForm()

    context = {
        "patient": patient,
        "medications": medications,
        "reports": reports,
        "report_form": report_form,
        "med_form": med_form,
        "med_search": med_search,
        "med_status": med_status,
        "report_search": report_search,
        "report_type": report_type,
    }
    return render(request, "doc/doc_patient_detail.html", context)


@login_required
@allowedUsers(["DOC"])
def edit_medication(request, med_id):
    medication = get_object_or_404(Medication, id=med_id)
    if request.method == "POST":
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            return redirect("DOC_PAT_DETAIL", patient_id=medication.patient.id)
    else:
        return redirect("DOC_PAT_DETAIL", patient_id=medication.patient.id)


@login_required
@allowedUsers(["DOC"])
def delete_medication(request, med_id):
    medication = get_object_or_404(Medication, id=med_id)
    patient_id = medication.patient.id
    if request.method == "POST":
        medication.delete()
        return redirect("DOC_PAT_DETAIL", patient_id=patient_id)
    # Optionally, render a confirmation page, but for now, just redirect if not POST
    return redirect("DOC_PAT_DETAIL", patient_id=patient_id)


@login_required
@allowedUsers(["DOC"])
def add_medication(request, pat_id):
    if request.method == "POST":
        doc = request.user.DOC
        form = MedicationForm(request.POST)
        print("-------------submit button------------")
        if form.is_valid():
            medication = form.save(commit=False)
            medication.patient = PatientRecord.objects.get(pk=pat_id)
            medication.doctor = doc
            medication.save()
            print("-----------saving----------")
            return redirect("DOC_PAT_DETAIL", patient_id=pat_id)
        print("-----------invalid form----------")
    else:
        form = MedicationForm()

    context = {"form": form, "id": pat_id, "action": "Add"}
    return render(request, "doc/doc_add_edit_medication.html", context)


@login_required
@allowedUsers(["DOC"])
def edit_vitals(request, patient_id):
    patient = get_object_or_404(PatientRecord, id=patient_id)
    if request.method == "POST":
        form = EditVitalsForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("DOC_PAT_DETAIL", patient_id=patient.id)
    else:
        return redirect("DOC_PAT_DETAIL", patient_id=patient.id)


@login_required
@allowedUsers(["DOC"])
def view_patient_report(request, patient_id, report_id):
    """View for doctors to view a specific patient report"""
    # Ensure the patient exists and is linked to the current doctor
    patient_list_entry = get_object_or_404(
        PatientsList, patient__id=patient_id, doctor=request.user.DOC
    )
    patient = patient_list_entry.patient

    # Get the specific report for this patient
    report = get_object_or_404(Report, id=report_id, patient=patient)

    context = {"report": report, "patient": patient}
    return render(request, "doc/doc_view_patient_report.html", context)


@login_required
@allowedUsers(["DOC"])
def add_patient_report(request, patient_id):
    """View for doctors to add new reports for their patients"""
    # Ensure the patient exists and is linked to the current doctor
    patient_list_entry = get_object_or_404(
        PatientsList, patient__id=patient_id, doctor=request.user.DOC
    )
    patient = patient_list_entry.patient

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.uploaded_by = request.user
            report.save()
            messages.success(request, "Report uploaded successfully!")
            return redirect("DOC_PAT_DETAIL", patient_id=patient.id)
        else:
            print("bhai report tohsahi daal")
            # Return to the patient detail page with the form errors
            return redirect("DOC_PAT_DETAIL", patient_id=patient.id)
    else:
        return redirect("DOC_PAT_DETAIL", patient_id=patient.id)


@login_required
@allowedUsers(["DOC"])
def get_report_edit_form(request, patient_id, report_id):
    """Get report data for edit modal"""
    # Ensure the patient exists and is linked to the current doctor
    patient_list_entry = get_object_or_404(
        PatientsList, patient__id=patient_id, doctor=request.user.DOC
    )
    patient = patient_list_entry.patient

    # Get the specific report and ensure the doctor uploaded it
    report = get_object_or_404(Report, id=report_id, patient=patient)

    # Check if the current doctor uploaded this report
    if report.uploaded_by != request.user:
        return JsonResponse(
            {"success": False, "error": "You can only edit reports that you uploaded."}
        )

    # Create form with instance
    form = ReportForm(instance=report)

    # Get form data
    form_data = {}
    for field_name, field in form.fields.items():
        if field_name == "file":
            # For file field, we don't send the actual file, just indicate it exists
            form_data[field_name] = {
                "value": report.file.name if report.file else "",
                "required": False,  # File is optional in edit mode
                "help_text": field.help_text,
                "label": field.label,
            }
        else:
            form_data[field_name] = {
                "value": form.initial.get(field_name, ""),
                "required": field.required,
                "help_text": field.help_text,
                "label": field.label,
            }

    return JsonResponse(
        {
            "success": True,
            "form_data": form_data,
            "report": {
                "id": report.id,
                "title": report.title,
                "report_type": report.report_type,
                "report_date": (
                    report.report_date.strftime("%Y-%m-%d")
                    if report.report_date
                    else ""
                ),
                "lab_facility": report.lab_facility or "",
                "description": report.description or "",
            },
        }
    )


@login_required
@allowedUsers(["DOC"])
def edit_patient_report(request, patient_id, report_id):
    """View for doctors to edit reports they uploaded"""
    # Ensure the patient exists and is linked to the current doctor
    patient_list_entry = get_object_or_404(
        PatientsList, patient__id=patient_id, doctor=request.user.DOC
    )
    patient = patient_list_entry.patient

    # Get the specific report and ensure the doctor uploaded it
    report = get_object_or_404(Report, id=report_id, patient=patient)

    # Check if the current doctor uploaded this report
    if report.uploaded_by != request.user:
        messages.error(request, "You can only edit reports that you uploaded.")
        return redirect("DOC_PAT_DETAIL", patient_id=patient.id)

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Report updated successfully!")
            return redirect("DOC_PAT_DETAIL", patient_id=patient.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        return redirect("DOC_PAT_DETAIL", patient_id=patient.id)


@login_required
@allowedUsers(["DOC"])
def delete_patient_report(request, patient_id, report_id):
    """View for doctors to delete reports they uploaded"""
    # Ensure the patient exists and is linked to the current doctor
    patient_list_entry = get_object_or_404(
        PatientsList, patient__id=patient_id, doctor=request.user.DOC
    )
    patient = patient_list_entry.patient

    # Get the specific report and ensure the doctor uploaded it
    report = get_object_or_404(Report, id=report_id, patient=patient)

    # Check if the current doctor uploaded this report
    if report.uploaded_by != request.user:
        messages.error(request, "You can only delete reports that you uploaded.")
        return redirect("DOC_PAT_DETAIL", patient_id=patient.id)

    if request.method == "POST":
        # Delete the file from storage
        if report.file:
            if os.path.exists(report.file.path):
                os.remove(report.file.path)

        report.delete()
        messages.success(request, "Report deleted successfully!")
        return redirect("DOC_PAT_DETAIL", patient_id=patient.id)

    context = {"report": report, "patient": patient}
    return render(request, "doc/doc_delete_report.html", context)


@login_required
@allowedUsers(["DOC"])
def downloadReport(request, patient_id, report_id):
    """View for patients to download their report files"""
    report = get_object_or_404(Report, id=report_id, patient__id=patient_id)

    if report.file:
        response = HttpResponse(report.file, content_type="application/octet-stream")
        response["Content-Disposition"] = (
            f'attachment; filename="{os.path.basename(report.file.name)}"'
        )
        return response
    else:
        messages.error(request, "File not found.")
        return redirect("DOC_PAT_DETAIL")


@login_required
@allowedUsers(["DOC"])
def doctor_appointments(request):
    scheduled = Appointment.objects.filter(
        doctor__user=request.user, status="scheduled"
    ).order_by("date_time")
    completed = Appointment.objects.filter(
        doctor__user=request.user, status="completed"
    ).order_by("date_time")
    cancelled = Appointment.objects.filter(
        doctor__user=request.user, status="cancelled"
    ).order_by("date_time")
    # Get the doctor's patients for the create appointment form
    patients = PatientsList.objects.filter(doctor=request.user.DOC)
    # Create the appointment form for the modal
    appointment_form = AppointmentForm()
    # Filter patient choices to only show connected patients
    appointment_form.fields["patient"].queryset = PatientRecord.objects.filter(
        id__in=patients.values_list("patient_id", flat=True)
    )
    now = timezone.now()
    context = {
        "scheduled": scheduled,
        "completed": completed,
        "cancelled": cancelled,
        "patients": patients,
        "appointment_form": appointment_form,
        "now": now,
    }
    return render(request, "doc/doctor_appointments.html", context)


@login_required
@allowedUsers(["DOC"])
def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = request.user.DOC
            appointment.save()
            messages.success(request, "Appointment created successfully!")
            return redirect("DOC_APOI")
        else:
            # If form is invalid, redirect back with error message
            messages.error(request, "Please correct the errors in the form.")
            return redirect("DOC_APOI")
    else:
        # If someone tries to access this URL directly, redirect to appointments page
        return redirect("DOC_APOI")


@login_required
@allowedUsers(["DOC"])
def edit_appointment(request, ap_id):
    appointment = get_object_or_404(Appointment, pk=ap_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect("DOC_APOI")
        else:
            messages.error(request, "Please correct the errors in the form.")
            return redirect("DOC_APOI")
    else:
        return redirect("DOC_APOI")


@login_required
@allowedUsers(["DOC"])
def get_appointment_data(request, ap_id):
    """Get appointment data for edit modal"""
    appointment = get_object_or_404(Appointment, pk=ap_id)

    # Convert to timezone-aware datetime if it's naive
    if timezone.is_naive(appointment.date_time):
        # If the datetime is naive, assume it's in the current timezone
        local_datetime = timezone.make_aware(
            appointment.date_time, timezone.get_current_timezone()
        )
    else:
        # If it's already timezone-aware, convert to current timezone
        local_datetime = timezone.localtime(appointment.date_time)

    return JsonResponse(
        {
            "success": True,
            "appointment": {
                "patient_id": appointment.patient.id,
                "date_time": local_datetime.strftime("%Y-%m-%dT%H:%M"),
                "hms_room_desc": appointment.hms_room_desc or "",
            },
        }
    )


@login_required
@allowedUsers(["DOC"])
def cancel_appointment(request, ap_id):

    appointment = get_object_or_404(Appointment, pk=ap_id)
    appointment.cancelled()

    return redirect("DOC_APOI")


@login_required
@allowedUsers(["DOC"])
def get_med_edit_form(request, patient_id, med_id):
    med = get_object_or_404(Medication, id=med_id, patient_id=patient_id)
    form = MedicationForm(instance=med)
    form_data = {}
    for name, field in form.fields.items():
        bound_field = form[name]
        field_type = "text"
        if hasattr(field, "choices") and field.choices:
            field_type = "select"
            choices = [{"value": c[0], "display": c[1]} for c in field.choices]
        elif field.widget.__class__.__name__ == "Textarea":
            field_type = "textarea"
            choices = []
        else:
            choices = []
        form_data[name] = {
            "label": bound_field.label,
            "value": bound_field.value(),
            "required": field.required,
            "type": field_type,
            "choices": choices,
        }
    return JsonResponse({"success": True, "form_data": form_data})


@login_required
@allowedUsers(["DOC"])
def get_edit_vitals_form(request, patient_id):
    patient = get_object_or_404(PatientRecord, id=patient_id)
    form = EditVitalsForm(instance=patient)
    form_data = {}
    for name, field in form.fields.items():
        bound_field = form[name]
        field_type = "number"
        if field.widget.__class__.__name__ == "Textarea":
            field_type = "textarea"
        form_data[name] = {
            "label": bound_field.label,
            "value": bound_field.value(),
            "required": field.required,
            "type": field_type,
        }
    return JsonResponse({"success": True, "form_data": form_data})
