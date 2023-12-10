from django import forms
from .models import ServiceLocations, Devices
from django.utils import timezone
from datetime import datetime, timedelta
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

class MonthYearForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MonthYearForm, self).__init__(*args, **kwargs)

        # Get current month and year
        today = datetime.now()
        current_month = today.month
        current_year = today.year

        # Create a list of tuples for months and years
        months_years = []
        for i in range(20):  # Display the last 15 months
            months_years.append((current_month, current_year))
            # Move to the previous month
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1
        # Generate choices for the select field
        choices = [(f"{year}-{month:02d}", f"{year} {datetime.strptime(str(month), '%m').strftime('%B')}") for month, year in months_years]        # Add choices to the form field
        self.fields['month_year'] = forms.ChoiceField(
            choices=choices,
            widget=forms.Select(attrs={'class': 'form-control', 'id': 'month-year-selector-id'}),
            label=False
        )