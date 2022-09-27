import imp
from django.shortcuts import render,redirect
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Company
from django.forms import ModelForm
from django.views.generic import  CreateView, FormView, TemplateView, UpdateView


class CompanyProfileForm(ModelForm):

    class Meta:
        model = Company
        exclude = ('user',)
        # widgets = {
        #     'date_of_birth': forms.DateInput(attrs = {'class':'form-control','type':'date'})
        # }
                
class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField()
        
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField( widget = forms.PasswordInput())

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(LoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user
