from django import forms
from .models import ServiceLocations, Devices
from django.utils import timezone
class ServiceLocationForm(forms.ModelForm):
    class Meta:
        model = ServiceLocations
        fields = '__all__'
        exclude = ['customer']
        customer = forms.IntegerField()
        widgets = {
            'unitNumber': forms.NumberInput(attrs={'class': 'form-control'}),
            'streetNumber': forms.NumberInput(attrs={'class': 'form-control'}),
            'streetName': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'sstate': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'serviceStart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'squareFootage': forms.NumberInput(attrs={'class': 'form-control'}),
            'noBedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'noOccupants': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DeviceCreationForm(forms.ModelForm):
    class Meta:
        model = Devices
        exclude = ['deviceID', 'location']  
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control'}),
            'device_type': forms.Select(attrs={'class': 'form-control'}),
            'modelNumber': forms.Select(attrs={'class': 'form-control'}),
        }
class DateSelectorForm(forms.Form):
    yesterday_date = (timezone.now() - timezone.timedelta(days=2)).strftime("%Y-%m-%d")  # Get yesterday's date
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'calendar-selector',
            'type': 'date',
            'placeholder': 'Select a date',
            'max': yesterday_date,  # Set the min attribute to yesterday's date
        }),
        label=False
    )