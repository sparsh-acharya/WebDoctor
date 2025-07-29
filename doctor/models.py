
# Create your models here.
from datetime import date, timedelta
from django.utils import timezone
import uuid
from django.db import models
from EHR import settings
from doctor.tasks import *
from hms import *
from EHR.celery import app

User = settings.AUTH_USER_MODEL

class DoctorProfile(models.Model):
    SPECIALIZATION_CHOICES = [
        ('CARDIOLOGY', 'Cardiology'),
        ('DERMATOLOGY', 'Dermatology'),
        ('ENDOCRINOLOGY', 'Endocrinology'),
        ('GASTROENTEROLOGY', 'Gastroenterology'),
        ('NEUROLOGY', 'Neurology'),
        ('ONCOLOGY', 'Oncology'),
        ('ORTHOPEDICS', 'Orthopedics'),
        ('PEDIATRICS', 'Pediatrics'),
        ('PSYCHIATRY', 'Psychiatry'),
        ('RADIOLOGY', 'Radiology'),
        ('SURGERY', 'Surgery'),
        ('GENERAL', 'General Medicine'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="DOC")
    uid = models.CharField(max_length=50, unique=True, editable=False, blank=True)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField()
    education = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = self.generate_unique_uid("DOCTOR")
        super().save(*args, **kwargs)

    def generate_unique_uid(self, prefix):
        while True:
            new_uid = f"{prefix}-{uuid.uuid4().hex[:10].upper()}"
            if not DoctorProfile.objects.filter(uid=new_uid).exists():
                return new_uid

    def __str__(self):
        return f"{self.uid} - Dr. {self.user.first_name} {self.user.last_name}"

    @property
    def full_name(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class PatientsList(models.Model):
    patient = models.ForeignKey('patients.PatientRecord', on_delete=models.CASCADE, help_text='patient model')
    doctor = models.ForeignKey('DoctorProfile', on_delete=models.CASCADE, help_text='doctor model')
    connect_date = models.DateTimeField(auto_now_add=True,help_text='date of connection')

    class Meta:
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"{self.patient.user.first_name} conected to {self.doctor.full_name} on {self.connect_date}"

class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey('patients.PatientRecord', on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    doc_meeting_link = models.URLField(blank=True)
    pat_meeting_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hms_room_id = models.CharField(max_length=128, blank=True, null=True)
    hms_room_name = models.CharField(max_length=128, blank=True, null=True)
    hms_room_desc = models.CharField(max_length=120, blank=True, null=True)
    task_id = models.CharField(max_length=255, blank=True, null=True)

    def completed(self):
        self.status = 'completed'
        self.save()

    def cancelled(self):
        app.control.revoke(self.task_id, terminate=True)
        self.status = 'cancelled'
        appointment_cancelled_task.delay(self.hms_room_id)
        self.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_date_time = None
        old_task_id = None

        if not self.hms_room_id:
            uid = uuid.uuid4().hex[:10].upper()
            self.hms_room_name = f"WebDoctor-Appointment-{uid}"
            self.hms_room_id = create_room(self.hms_room_name)

        if not self.doc_meeting_link:
            self.doc_meeting_link = generate_link_for_role(self.hms_room_id, "host")

        if not self.pat_meeting_link:
            self.pat_meeting_link = generate_link_for_role(self.hms_room_id, "guest")

        # Save first if new, so we have a PK and all fields are set
        if is_new:
            super().save(*args, **kwargs)

        if not is_new:
            orig = Appointment.objects.get(pk=self.pk)
            old_date_time = orig.date_time
            old_task_id = orig.task_id

        if is_new or (old_date_time and old_date_time != self.date_time):
            # Revoke old task if it exists
            if old_task_id:
                app.control.revoke(old_task_id, terminate=True)
            # Schedule new task
            run_at = self.date_time + timedelta(minutes=30)
            result = appointment_completed_task.apply_async((self.hms_room_id,self.pk), eta=run_at)
            self.task_id = result.id
            # Save the new task ID
            super().save()

        # For updates to other fields, call super().save() only if not already called above
        if not is_new and not (old_date_time and old_date_time != self.date_time):
            super().save(*args, **kwargs)

    @property
    def is_active(self):
        if self.status == 'scheduled':
            return timezone.now() >= self.date_time
        return False

    def is_today(self):
        return date.today() == self.date_time.date()
    def __str__(self):
        return f"{self.hms_room_name} - {self.status}"
