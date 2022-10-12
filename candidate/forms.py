from .models import CandidateProfile, LatEducation, Experience, JobApplication
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class CandidateProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=DateInput())

    class Meta:
        model = CandidateProfile
        fields = ["candidate_image", "summary", "dob", "resume", "skills", "address", "state", "country",
                  "languages_known"]
        # exclude = ("user", "latest_edu", "experience",)
        widgets = {
            "summary": forms.Textarea(attrs={"class": "form-control"}),
            "dob" : forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-select"}),
            "languages_known": forms.TextInput(attrs={"class": "form-control"}),
        }


class LatEducationForm(forms.ModelForm):
    class Meta:
        model = LatEducation
        fields = "__all__"


class ExperienceForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Experience
        exclude = ('candidate',)

