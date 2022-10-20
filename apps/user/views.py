from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator

from apps.user import forms
from apps.accounts.models import User
from apps.accounts.verified_access import login_required


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
            messages.error(self.request, "Registration Failed")
            return render(request, "jobseeker/registration.html", context={"form": form})


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
                    return redirect('myaccount')
                else:
                    messages.info(request, "Credentials did not match with user account")
                    return redirect("company-login")
            else:
                messages.error(request, "Invalid Credentials")
                print("No such User")
        else:
            messages.error(request, "Error in Form")
            print("Form Error")

        return render(request, "jobseeker/login.html", context={"form": form})


@method_decorator(login_required, name="dispatch")
class LogOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")


@method_decorator(login_required,name="dispatch")
class MyAccountView(TemplateView):

    def get(self, request, *args, **kwargs):

        return render(request, "jobseeker/welcome.html")
