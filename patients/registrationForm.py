from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PatientRecord
from user.models import CustomUser

class PatientRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': '+1 (555) 123-4567'
        })
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary'
        })
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender')] + list(CustomUser._meta.get_field('gender').choices),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary resize-none',
            'rows': '3',
            'placeholder': 'Enter your full address'
        }),
        required=True
    )
    emergency_contact_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': '+1 (555) 987-6543'
        })
    )

    class Meta:
        model = CustomUser
        fields = ["first_name","last_name","email", "phone_number", "date_of_birth", "gender", "address", "emergency_contact_number", "password1", "password2"]
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'address': 'Address',
            'emergency_contact_number': 'Emergency Contact Number',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        help_texts = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'email': 'Enter a valid email address',
            'phone_number': 'Enter your contact phone number',
            'date_of_birth': 'Select your date of birth',
            'gender': 'Select your gender',
            'address': 'Enter your complete address',
            'emergency_contact_number': 'Enter emergency contact phone number',
            'password1': 'Create a strong password',
            'password2': 'Confirm your password',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to all form fields
        for field_name, field in self.fields.items():
            if field_name not in ['phone_number', 'date_of_birth', 'gender', 'address', 'emergency_contact_number']:
                if isinstance(field.widget, forms.TextInput):
                    field.widget.attrs.update({
                        'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                        'placeholder': self.get_placeholder(field_name)
                    })
                elif isinstance(field.widget, forms.EmailInput):
                    field.widget.attrs.update({
                        'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                        'placeholder': 'john.doe@example.com'
                    })
                elif isinstance(field.widget, forms.PasswordInput):
                    field.widget.attrs.update({
                        'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
                        'placeholder': '••••••••'
                    })

    def get_placeholder(self, field_name):
        placeholders = {
            'first_name': 'John',
            'last_name': 'Doe',
        }
        return placeholders.get(field_name, '')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            try:
                PatientRecord.objects.create(
                    user=user,
                    emergency_contact_number=self.cleaned_data["emergency_contact_number"],
                )
            except Exception as e:
                user.delete()  # Delete the user if PatientRecord creation fails
                raise e  # Re-raise the exception to notify the error

        return user
