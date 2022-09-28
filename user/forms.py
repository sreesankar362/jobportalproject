from django import forms
from user.models import ApplicantUser

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = ApplicantUser
        fields = ["username", "first_name", "last_name", "password", "email", "mobile", "bio", "location",
                  "gender", "dob","profile_pic"]

    widgets = {
        "dob": forms.DateInput(attrs={"class": "form-control"}),
        "mobile": forms.NumberInput(attrs={"class": "form-control"}),
        "location": forms.TextInput(attrs={"class": "form-control"}),
        "bio": forms.Textarea(attrs={"class": "form-control"})
    }
