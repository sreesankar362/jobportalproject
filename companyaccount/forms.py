from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Company
from django.contrib.auth.forms import UserCreationForm



class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name','company_email','phone']


class CompanyUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'create password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'confirm password'}),
    )
    class Meta:
        model = User
        fields = ['username', 'password1','password2']
