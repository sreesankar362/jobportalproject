from django import forms
from user.models import ApplicantUser


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(forms.ModelForm):
    dob = forms.DateField(widget=DateInput())
    class Meta:
        model = ApplicantUser
        fields = ["username", "password", "first_name", "last_name", "email", "dob", "mobile", "bio", "location",
                  "gender", "profile_pic"]

    widgets = {

        "mobile": forms.NumberInput(attrs={"class": "form-control"}),
        "location": forms.TextInput(attrs={"class": "form-control"}),
        "bio": forms.Textarea(attrs={"class": "form-control"}),
        "password": forms.PasswordInput(attrs={"class": "form-control"})
    }
