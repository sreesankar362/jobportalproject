from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from user.models import ApplicantUser
from user import forms
from django.contrib.auth import authenticate, login, logout


class RegistrationView(View):

    """
    For collecting and storing applicant information . Used custom Model ApplicantUser
    """
    def get(self, request, *args, **kwargs):
        form = forms.RegistrationForm()
        return render(request, "user/registration.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = forms.RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                applicant = ApplicantUser.objects.create_user(**form.cleaned_data)
            except:
                print("Error in your data")
                return render(request, "user/registration.html", context={"form": form})
            return redirect("home")
        else:
            print("........Form Error.......")
            return render(request,"user/registration.html",context={"form": form})

        return render(request, "user/login.html")


class LogInView(View):
    """
    User Login call reaches here.Authenticate user with username and password.
    """
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, "user/login.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get("username"),
                                password=form.cleaned_data.get("password"))
            if user:
                login(request, user)
                print("Logged success")
                return redirect("welcome")
            else:
                print("failure")
                return render(request, "user/login.html", context={"form": form})
        return render(request, "user/registration.html")


class LogOutView(View):
    """
    User can Logout by clicking a button
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        print("loggged out Successfully")
        return redirect("home")


class WelcomeView(TemplateView):
    """
    Delete once real code used
    """
    def get(self, request, *args, **kwargs):
        user = ApplicantUser.objects.get(username=request.user)
        print(user.profile_pic.url)
        return render(request, "user/welcome.html", context={"user": user})
