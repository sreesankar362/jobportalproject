from django import forms
from .models import JobModel,Enquiry


class JobModelForm(forms.ModelForm):
    class Meta:
        model = JobModel
        exclude = ('company', 'is_active')


class JobSearchForm(forms.Form):
    keyword = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Job Title/Keyword or Company'}),
    )
    location = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Location'}),
    )


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = "__all__"

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control"}),
        }

