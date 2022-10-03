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



