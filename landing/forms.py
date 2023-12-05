from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Customer

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'billing_unit_number', 'billing_street_number', 'billing_street_name', 'billing_city', 'billing_state', 'billing_zipcode')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_unit_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'billing_street_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'billing_street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_city': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_state': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_zipcode': forms.TextInput(attrs={'class': 'form-control'}),
        }
