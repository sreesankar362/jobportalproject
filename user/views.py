from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from user import forms
from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from accounts.utils import detectuser
from django.contrib import messages

class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = forms.RegistrationForm()
        return render(request, "jobseeker/registration.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            # create user using form
            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.JOBSEEKER
            user.save()
            messages.success(self.request, "Registered as a Job Seeker")
            return redirect('login')
        else:
            print("Error..................................")
            messages.error(self.request, "Error in Registration")
            return render(request, "home/home.html")


class LogInView(View):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, "jobseeker/login.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                print("logged In Successfully")
                if user.role == 2:
                    login(request, user)
                    messages.success(request,"Welcome to your Dashboard")
                    return redirect('myaccount')
                else:
                    return redirect("company-login")
            else:
                messages.error(request,"No such User")
                print("No such User")
        else:
            messages.error(request,"Error in Form")
            print("Form Error")

        return render(request, "jobseeker/registration.html",{"form":form})


class LogOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        print("logged out Successfully")
        messages.success(request,"See You Later")
        return redirect("home")


class MyAccountView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, "jobseeker/welcome.html")
