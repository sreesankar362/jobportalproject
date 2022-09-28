from django import forms

from .models import JobModel


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobModel
        exclude = ('company', 'is_active')
        widgets = {
            'position': forms.TextInput(attrs={"class": "form-control", "placeholder": "Job Position"}),
            'job_description': forms.Textarea(attrs={"class": "form-control", "placeholder": "Job Description"}),
            'skills': forms.Textarea(attrs={"placeholder": "Skills Required"}),

        }

