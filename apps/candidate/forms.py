from django.forms import modelformset_factory, DateInput, TextInput, NumberInput,ClearableFileInput

from .models import CandidateProfile, LatEducation, Experience



class DateInput(DateInput):
    input_type = 'date'


EduFormSet = modelformset_factory(
    LatEducation, fields=("qualification","institute","university","percent","passed_year"), extra=1, widgets={
        "qualification": TextInput(attrs={"class": "form-control"}),
        "institute": TextInput(attrs={"class": "form-control"}),
        "university": TextInput(attrs={"class": "form-control"}),
        "percent": NumberInput(attrs={"class": "form-control"}),
        "passed_year": NumberInput(attrs={"class": "form-control"}),
    }
)
ExpFormSet = modelformset_factory(
    Experience, fields=("experience_field", "job_position", "company", "experience_describe", "start_date", "end_date"),
    extra=1, widgets={
        "start_date": DateInput(attrs={"class": "form-control", "type": "date"}),
        "end_date": DateInput(attrs={"class": "form-control", "type": "date"}),
        "experience_field": TextInput(attrs={"class": "form-control"}),
        "job_position": TextInput(attrs={"class": "form-control"}),
        "company": TextInput(attrs={"class": "form-control"}),

    }
)
CandidateFormSet = modelformset_factory(
    CandidateProfile, fields=("candidate_image", "summary", "dob", "resume", "skills", "address", "state", "country",
                              "languages_known"), extra=1,
    widgets={"dob": DateInput(attrs={"class": "form-control", "type": "date"}),
             "skills": TextInput(attrs={"class": "form-control"}),
             "state": TextInput(attrs={"class": "form-control"}),
             "resume": ClearableFileInput(attrs={"class": "form-control"}),
             "languages_known": TextInput(attrs={"class": "form-control"}),

             }
)
