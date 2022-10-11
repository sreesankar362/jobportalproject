from .models import CandidateProfile, LatEducation, Experience,Skill
from django import forms
from django.forms import modelformset_factory

class DateInput(forms.DateInput):
    input_type = 'date'


class CandidateProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=DateInput())

    class Meta:
        model = CandidateProfile
        fields = ["dob", "resume", "location", "country"]
    # exclude = ("user", "latest_edu", "experience",)


class LatEducationForm(forms.ModelForm):
    class Meta:
        model = LatEducation
        fields = "__all__"


class ExperienceForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Experience
        fields = "__all__"


class SkillForm(forms.ModelForm):
    class Meta:
        model=Skill
        fields = ["skill"]