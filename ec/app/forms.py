from django import forms
from django.utils import timezone
from . import models

#Create your forms here

class WarehousesForm(forms.ModelForm): #This form will serve two purposes. Create and edit warehouses!
    class Meta:
        model = models.warehouse
        fields = ['address', 'city', 'postal_code', 'country']

        labels = {
            'address': 'Address',
            'city': 'City',
            'postal_code': 'Postal Code',
            'country': 'Country',
        }

        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
            'city': forms.TextInput(attrs={}),
            'postal_code': forms.TextInput(attrs={}),
            'country': forms.TextInput(attrs={}),
        }

        for field in fields:
            widgets[field].attrs['required'] = 'required'

class SupplierForm(forms.ModelForm): #This form will serve two purposes. Create and edit suppliers!
    class Meta:
        model = models.supplier
        fields = ['name', 'phone_number', 'email', 'warehouse']

        labels = {
            'name': 'Supplier Name',
            'phone_number': 'Phone Number',
            'email': 'Email',
            'warehouse': 'Warehouses',
        }

        widgets = {
            'name': forms.TextInput(attrs={}),
            'phone_number': forms.TextInput(attrs={}),
            'email': forms.EmailInput(attrs={}),
            'warehouse': forms.CheckboxSelectMultiple(attrs={}),
        }
        
        for field in fields:
            widgets[field].attrs['required'] = False  # Set required to False for all fields

    def clean_warehouse(self):
        warehouse = self.cleaned_data.get('warehouse')
        if not warehouse:  # Allow the checkbox to be unchecked
            return []
        return warehouse


class ComponentTypeForm(forms.ModelForm): #This form will serve two purposes. Create and edit component types!
    class Meta:
        model = models.component_type
        fields = ['type_name', 'description']

        labels = {
            'type_name': 'Component Type',
            'description': 'Description'
        }

        widgets = {
            'type_name': forms.TextInput(attrs={}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        }
        
        for field in fields:
            widgets[field].attrs['required'] = 'required'

class ComponentForm(forms.ModelForm): #This form will serve two purposes. Create and edit components!
    class Meta:
        model = models.components
        fields = ['name', 'component_type', 'serial_number', 'purchase_date', 'purchase_price', 'supplier', 'image']
        
        labels = {
            'name': 'Name',
            'component_type': 'Type',
            'serial_number': 'Serial Nº',
            'purchase_date': 'Purchase Date',
            'purchase_price': 'Purchase Price',
            'supplier': 'Supplier',
            'image': 'Product Image'
        }

        widgets = {
            'name': forms.TextInput(attrs={}),
            'component_type': forms.Select(attrs={}),
            'serial_number': forms.TextInput(attrs={}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'purchase_price': forms.NumberInput(attrs={}),
            'supplier': forms.Select(attrs={}),
            'image': forms.Textarea(attrs={'rows': 2, 'cols': 30, 'placeholder': 'Enter image URL'})
        }

        for field in fields:
            widgets[field].attrs['required'] = False

class EquipmentTypeForm(forms.ModelForm): #This form will serve two purposes. Create and edit equipment types!
    class Meta:
        model = models.equipment_type
        fields = ['type_name', 'description']

        labels = {
            'type_name': 'Equipment Type',
            'description': 'Description'
        }

        widgets = {
            'type_name': forms.TextInput(attrs={}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        }
        
        for field in fields:
            widgets[field].attrs['required'] = 'required'

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = models.equipments
        fields = ['type', 'name', 'serial_number', 'value', 'components']

        labels = {
            'type': 'Equipment Type',
            'name': 'Equipment Name',
            'serial_number': 'Serial Number',
            'value': 'Equipment Value',
        }

        widgets = {
            'name': forms.TextInput(attrs={}),
            'type': forms.Select(attrs={}),
            'serial_number': forms.TextInput(attrs={}),
            'value': forms.NumberInput(attrs={}),
            'components': forms.CheckboxSelectMultiple(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['components'].queryset = models.components.objects.all()

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'required'}))

    class Meta:
        model = models.users
        fields = ['first_name', 'last_name', 'email', 'password']

        labels = {
            'email': 'Email',
            'password': 'Password',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }

        widgets = {
            'email': forms.EmailInput(attrs={}),
            'password': forms.PasswordInput(attrs={}),
            'first_name': forms.TextInput(attrs={}),
            'last_name': forms.TextInput(attrs={}),
        }

        for field in fields:
            widgets[field].attrs['required'] = 'required'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.users
        fields = ['email', 'password']

        labels = {
            'email': 'Email',
            'password': 'Password',
        }

        widgets = {
            'email': forms.EmailInput(attrs={}),
            'password': forms.PasswordInput(attrs={}),
        }

        for field in fields:
            widgets[field].attrs['required'] = 'required'
    def clean_email(self):
        email = self.cleaned_data['email']
        print(f'Cleaned email: {email}')
        return email