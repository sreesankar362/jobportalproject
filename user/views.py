from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView
from user import forms
from accounts.models import User
from django.contrib.auth import authenticate,login,logout
from accounts.utils import detectuser


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form = forms.RegistrationForm()
        return render(request,"jobseeker/registration.html",context={"form": form})

    def post(self,request,*args,**kwargs):

        form = forms.RegistrationForm(request.POST)
        if form.is_valid():

            # create user using form
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.JOBSEEKER
            user.save()
            return redirect('jobs')
        else:
            print("Error..................................")
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
                if user.role == 2:
                    login(request, user)
                    return redirect('jobs')
            else:
                return redirect("company-login")

        return render(request, "jobseeker/registration.html")


class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        print("logged out Successfully")
        return redirect("home")


class MyAccountView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "jobseeker/welcome.html")


