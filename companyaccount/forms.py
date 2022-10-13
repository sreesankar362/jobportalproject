from django import forms
from companyaccount.models import CompanyProfile
from accounts.models import User
from user.forms import RegistrationForm


class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name']
        
        widgets = {
            "company_name": forms.TextInput(attrs={"class":"form-control"})
        }


class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ('user', 'is_approved', 'social_profile', 'is_mail_verified', 'is_activated')
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "company_logo": forms.FileInput(attrs={"class": "form-control"}),
            "company_description": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "industry": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "team_size": forms.TextInput(attrs={"class": "form-control"}),
            "founded": forms.TextInput(attrs={"class": "form-control"}),
            "company_address": forms.TextInput(attrs={"class": "form-control"}),
        }


