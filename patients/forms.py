from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'report_type', 'report_date', 'file', 'description', 'lab_facility']
        labels = {
            'title': 'Report Title',
            'report_type': 'Report Type',
            'report_date': 'Test/Procedure Date',
            'file': 'Report File',
            'description': 'Description',
            'lab_facility': 'Laboratory/Facility'
        }
        help_texts = {
            'title': 'Enter a descriptive title for the report',
            'report_type': 'Select the type of medical report',
            'report_date': 'Date when the test or procedure was performed',
            'file': 'Upload the report file (PDF, images, or documents)',
            'description': 'Additional notes or description about the report',
            'lab_facility': 'Name of the laboratory or medical facility'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Enter report title'
            }),
            'report_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Select report type'
            }),
            'report_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'type': 'date'
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'rows': 4,
                'placeholder': 'Enter additional description or notes about the report'
            }),
            'lab_facility': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                'placeholder': 'Laboratory or facility name'
            })
        }
