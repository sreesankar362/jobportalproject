from .models import CandidateProfile, LatEducation, Experience
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class CandidateProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=DateInput())

    class Meta:
        model = CandidateProfile
        fields = ["candidate_image", "summary", "dob", "resume", "address", "country", "state",
                  "languages_known", "skills"]
    # exclude = ("user", "latest_edu", "experience",)


class LatEducationForm(forms.ModelForm):
    class Meta:
        model = LatEducation
        exclude = "__all__"


class ExperienceForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Experience
        exclude = ('candidate', 'exp_duration',)


