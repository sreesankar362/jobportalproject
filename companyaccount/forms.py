from django import forms
from companyaccount.models import Company
from django.contrib.auth.models import User

class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["company_name", "company_email"]
        widgets = {
            "company_name": forms.TextInput(attrs={"class":"form-control"}),
            "company_email": forms.EmailInput(attrs={"class": "form-control"})
        }

class CompanyUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget= forms.TextInput(attrs={"class":"form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget= forms.PasswordInput(attrs={"class":"form-control"})
    )
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control"})
        }


