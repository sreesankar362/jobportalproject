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