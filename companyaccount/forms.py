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


#nikhil
class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField()


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ('user', 'is_approved', 'social_profile', 'is_mail_verified')