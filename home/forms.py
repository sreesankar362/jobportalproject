from django import forms

from .models import JobModel


class JobPostForm(forms.ModelForm):
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