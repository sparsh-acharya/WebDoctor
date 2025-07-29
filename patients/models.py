import uuid
from django.db import models
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from doctor.tasks import appointment_completed_task
from hms import *
from EHR.celery import app
User = get_user_model()

class PatientRecord(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="PAT")
    uid = models.CharField(max_length=50, unique=True, editable=False, blank=True, help_text="Unique identifier for the patient record")
    emergency_contact_number = models.CharField(max_length=15, help_text="Emergency contact phone number")
    chronic_conditions = models.JSONField(null=True, blank=True, help_text="List of chronic medical conditions")
    blood_type = models.CharField(max_length=3, null=True, choices=BLOOD_TYPE_CHOICES, help_text="Select the patient's blood type")
    height = models.FloatField(null=True, help_text="Height in centimeters")
    weight = models.FloatField(null=True, help_text="Weight in kilograms")
    body_temperature = models.FloatField(null=True, help_text="Body temperature in Celsius")
    heart_rate = models.IntegerField(null=True, help_text="Heart rate in beats per minute")
    respiratory_rate = models.IntegerField(null=True, help_text="Respiratory rate in breaths per minute")

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = self.generate_unique_uid("PATIENT")
        super().save(*args, **kwargs)

    def generate_unique_uid(self, prefix):
        while True:
            new_uid = f"{prefix}-{uuid.uuid4().hex[:10].upper()}"
            if not PatientRecord.objects.filter(uid=new_uid).exists():
                return new_uid

    def __str__(self):
        return f"{self.uid} - {self.user.first_name}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def age(self):
        dob = getattr(self.user, 'date_of_birth', None)
        if dob is None:
            return None
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class PatientConnectionRequest(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
    ]

    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name='requests', help_text="Patient making the request")
    doctor = models.ForeignKey('doctor.DoctorProfile', on_delete=models.CASCADE, related_name='patient_requests', help_text="Doctor to whom the request is made")
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='PENDING', help_text="Current status of the request")
    request_date = models.DateTimeField(auto_now_add=True, help_text="Date and time when the request was created")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the request")

    class Meta:
        ordering = ['-request_date']
        verbose_name = "Patient Request"
        verbose_name_plural = "Patient Requests"

    def __str__(self):
        return f"Request from {self.patient.user.first_name} to Dr. {self.doctor.user.last_name} - {self.request_status}"


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('BLOOD_TEST', 'Blood Test'),
        ('X_RAY', 'X-Ray'),
        ('MRI', 'MRI'),
        ('CT_SCAN', 'CT Scan'),
        ('ULTRASOUND', 'Ultrasound'),
        ('ECG', 'ECG'),
        ('ECHO', 'Echocardiogram'),
        ('BIOPSY', 'Biopsy'),
        ('PATHOLOGY', 'Pathology'),
        ('OTHER', 'Other'),
    ]

    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name='reports', help_text="Patient who owns this report")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_reports', null=True, blank=True, help_text="User who uploaded this report")
    title = models.CharField(max_length=200, help_text="Title of the report")
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, help_text="Type of medical report")
    report_date = models.DateField(help_text="Date when the test/procedure was conducted")
    uploaded_date = models.DateTimeField(auto_now_add=True, help_text="Date when report was uploaded")
    file = models.FileField(upload_to='patient_reports/', help_text="Upload the report file (PDF, Image, etc.)")
    description = models.TextField(blank=True, null=True, help_text="Additional description or notes about the report")
    lab_facility = models.CharField(max_length=200, blank=True, null=True, help_text="Laboratory or facility where test was conducted")

    class Meta:
        ordering = ['-report_date', '-uploaded_date']
        verbose_name = "Patient Report"
        verbose_name_plural = "Patient Reports"

    def __str__(self):
        return f"{self.title} - {self.patient.full_name} ({self.report_date})"

    @property
    def file_extension(self):
        """Get the file extension for display purposes"""
        if self.file:
            return self.file.name.split('.')[-1].upper()
        return None

    @property
    def file_size_mb(self):
        """Get file size in MB"""
        if self.file:
            return round(self.file.size / (1024 * 1024), 2)
        return 0

class Medication(models.Model):
    status_choices = [
        ('ACTIVE', 'Active'),
        ('DISCONTINUED', 'Discontinued'),
    ]
    name = models.CharField(max_length=50,help_text="name of the medicine",default="")
    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name='medication')
    doctor = models.ForeignKey('doctor.DoctorProfile', on_delete=models.CASCADE, related_name='written_prescriptions')
    date_issued = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=timezone.now, help_text="When the patient should start taking the medication")
    duration = models.PositiveIntegerField(help_text="Duration in days to take the medication")
    dosage = models.PositiveIntegerField(help_text="e.g. 100mg ")
    frequency = models.CharField(max_length=100,help_text="eg. Twice a day",default="")
    status = models.CharField(max_length=20, choices=status_choices, default='ACTIVE', help_text="Current status of the medicine")


    @property
    def end_date(self):
        if self.start_date and self.duration:
            return self.start_date + timezone.timedelta(days=self.duration)
        return None

    def __str__(self):
        return f"Prescription for {self.patient} by Dr. {self.doctor} on {self.date_issued.date()}"
