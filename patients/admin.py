from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(PatientRecord)
admin.site.register(PatientConnectionRequest)
admin.site.register(Medication)
admin.site.register(Report)
