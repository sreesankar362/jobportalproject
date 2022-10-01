
from django import forms
from companyaccount.models import CompanyProfile
from accounts.models import User



class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name']

