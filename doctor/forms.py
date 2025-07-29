from django import forms
from doctor.models import Appointment
from patients.models import *

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'frequency', 'start_date', 'duration', 'status']
        labels = {
            'name': 'Medication Name',
            'dosage': 'Dosage (mg)',
            'frequency': 'Frequency',
            'start_date': 'Start Date',
            'duration': 'Duration (days)',
            'status': 'Status',
        }
        help_texts = {
            'name': 'Enter the name of the medication',
            'dosage': 'Specify the dosage amount in mg (e.g. 100)',
            'frequency': 'How often should the medication be taken (e.g. Twice a day)',
            'start_date': 'When to start taking this medication',
            'duration': 'How many days to take this medication',
            'status': 'Current status of the medication',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Enter medication name'
            }),
            'dosage': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'amount in mg (e.g. 100)'
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'e.g. Twice a day'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'e.g. 7'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary'
            }),
        }

class EditVitalsForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['height', 'weight', 'body_temperature', 'heart_rate', 'respiratory_rate']
        labels = {
            'height': 'Height',
            'weight': 'Weight',
            'body_temperature': 'Body Temperature',
            'heart_rate': 'Heart Rate',
            'respiratory_rate': 'Respiratory Rate',
        }
        help_texts = {
            'height': 'Patient height in centimeters',
            'weight': 'Patient weight in kilograms',
            'body_temperature': 'Body temperature in Celsius',
            'heart_rate': 'Heart rate in beats per minute',
            'respiratory_rate': 'Respiratory rate in breaths per minute',
        }
        widgets = {
            'height': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'step': '0.1',
                'placeholder': 'Height in cm'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'step': '0.1',
                'placeholder': 'Weight in kg'
            }),
            'body_temperature': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'step': '0.1',
                'placeholder': 'Body temperature in °C'
            }),
            'heart_rate': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Heart rate in bpm'
            }),
            'respiratory_rate': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Respiratory rate in breaths/min'
            }),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date_time','hms_room_desc']
        labels = {
            'patient': 'Select Patient',
            'date_time': 'Appointment Date & Time',
            'hms_room_desc': 'Description',
        }
        help_texts = {
            'patient': 'Choose a patient from your connected patients list',
            'date_time': 'Select the date and time for the appointment',
            'hms_room_desc': 'Reason for appointment',
        }
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Select a patient'
            }),
            'date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary'
            }),
            'hms_room_desc': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'eg:- Regular checkup'
            }),
        }
