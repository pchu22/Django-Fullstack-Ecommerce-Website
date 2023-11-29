from django import forms
from . import models

#Create your forms here

class ComponentForm(forms.ModelForm): #This form will serve two purposes. Create and edit components!
    class Meta:
        model = models.components
        fields = ['name', 'component_type', 'serial_number', 'purchase_date', 'purchase_price', 'supplier']
        
        labels = {
            'name': 'Name',
            'component_type': 'Type',
            'serial_number': 'Serial Nº',
            'purchase_date': 'Purchase Date',
            'purchase_price': 'Purchase Price',
            'supplier': 'Supplier',
        }

        widgets = {
            'name': forms.TextInput(attrs={}),
            'component_type': forms.Select(attrs={}),
            'serial_number': forms.TextInput(attrs={}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'purchase_price': forms.NumberInput(attrs={}),
            'supplier': forms.Select(attrs={}),
        }

        for field in fields:
            widgets[field].attrs['required'] = 'required'