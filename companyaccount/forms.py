from django.contrib.auth.models import User
from dataclasses import fields
import imp
from xml.etree.ElementInclude import include
from django.shortcuts import render,redirect
from django.contrib import messages
from django import forms
from betterforms.multiform import MultiForm
from betterforms.multiform import MultiModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CompanyProfile, SocialProfile
from django.forms import ModelForm
from django.views.generic import  CreateView, FormView, TemplateView, UpdateView
from user.forms import RegistrationForm


class CompanyProfileForm(ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ('user','is_approved','social_profile')
        
        
# class SocialProfileForm(ModelForm):
#     class Meta:
#         model = SocialProfile
#         fields = "__all__"

        
# class CompanyProfileMultiForm(MultiModelForm):
#     form_classes = {
#         'company': CompanyProfileForm,
#         'social': SocialProfileForm,
#     }

#     def save(self, commit=True):
#         objects = super(CompanyProfileMultiForm, self).save(commit=False)

#         if commit:
#             user = objects['company']
#             user.save()
#             profile = objects['social']
#             profile.user = user
#             profile.save()

#         return objects


class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField()
        
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField( widget = forms.PasswordInput())
    


class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name']
        
        widgets = {
            "company_name": forms.TextInput(attrs={"class":"form-control"})
        }