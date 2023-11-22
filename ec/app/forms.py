from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ResetPasswordEmailForm(PasswordChangeForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus': 'True', 'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))