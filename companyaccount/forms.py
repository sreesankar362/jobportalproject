<<<<<<< HEAD
from django.contrib.auth.models import User
from dataclasses import fields
import imp
from xml.etree.ElementInclude import include
from django.shortcuts import render,redirect
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Company, SocialProfile
from django.forms import ModelForm
from django.views.generic import  CreateView, FormView, TemplateView, UpdateView

class CompanyProfileForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('user','company_name','is_mail_verified',)
        
class SocialProfileForm(ModelForm):
    class Meta:
        model = SocialProfile
        # exclude = ()
        fields = "__all__"


class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField()
        
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField( widget = forms.PasswordInput())

# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(
#         label="Password",
#         strip=False,
#         widget=forms.PasswordInput,
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user = None
#         self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
#         self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

#     def clean(self, *args, **kwargs):
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")

#         if email and password:
#             self.user = authenticate(email=email, password=password)

#             if self.user is None:
#                 raise forms.ValidationError("User Does Not Exist.")
#             if not self.user.check_password(password):
#                 raise forms.ValidationError("Password Does not Match.")
#             if not self.user.is_active:
#                 raise forms.ValidationError("User is not Active.")

#         return super(LoginForm, self).clean(*args, **kwargs)

#     def get_user(self):
#         return self.user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField( widget = forms.PasswordInput())

||||||| 1613bdc
from django import forms
from companyaccount.models import Company
from django.contrib.auth.models import User
=======
from django import forms
from companyaccount.models import CompanyProfile
from accounts.models import User
from user.forms import RegistrationForm

>>>>>>> f41c6a974fcd56f57609f9cfd08ee6b068f9481a

class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name']
        
        widgets = {
            "company_name": forms.TextInput(attrs={"class":"form-control"})
        }

<<<<<<< HEAD
class CompanyUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget= forms.TextInput(attrs={"class":"form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget= forms.PasswordInput(attrs={"class":"form-control"})
    )
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control"})
        }
    def clean(self):
        cleaned_data = super(CompanyUserForm,self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("passwords does not match")

||||||| 1613bdc
class CompanyUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget= forms.TextInput(attrs={"class":"form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget= forms.PasswordInput(attrs={"class":"form-control"})
    )
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class":"form-control"})
        }
    def clean(self):
        cleaned_data = super(CompanyUserForm,self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("passwords does not match")



=======


>>>>>>> f41c6a974fcd56f57609f9cfd08ee6b068f9481a
