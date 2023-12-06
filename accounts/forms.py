from django import forms
from .models import ServiceLocations
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
            'sstate': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'serviceStart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'squareFootage': forms.NumberInput(attrs={'class': 'form-control'}),
            'noBedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'noOccupants': forms.NumberInput(attrs={'class': 'form-control'}),
        }
