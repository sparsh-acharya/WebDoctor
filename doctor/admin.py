from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(PatientsList)
admin.site.register(Appointment)
