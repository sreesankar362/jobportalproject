from django import forms

from .models import JobModel


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobModel
        exclude = ('company', 'is_active')


