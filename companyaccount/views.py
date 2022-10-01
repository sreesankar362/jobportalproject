from django.shortcuts import render,redirect
from django.views.generic import View
from companyaccount.forms import CompanyRegistrationForm
from user.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from.models import CompanyProfile

from django.contrib import messages
from accounts.models import User


class CompanyRegistrationView(View):
    def get(self, request, *args, **kwargs):
        company_form = CompanyRegistrationForm()
        company_user_form = RegistrationForm()
        context = {
            "company_form": company_form,
            "company_user_form": company_user_form
        }
        return render(request, "company/company_registration.html", context)

    def post(self, request, *args, **kwargs):
        company_form = CompanyRegistrationForm(request.POST)
        company_user_form = RegistrationForm(request.POST)

        if company_form.is_valid() and company_user_form.is_valid():
            company_name = company_form.cleaned_data["company_name"]
            password = company_user_form.cleaned_data['password']
            user_obj = company_user_form.save(commit=False)
            user_obj.set_password(password)
            user_obj.role = User.EMPLOYER
            user_obj.save()
            # company = CompanyProfile(company_name=company_name)
            # company.save()
            company_obj = company_form.save(commit=False)
            company_obj.user = user_obj

            messages.success(request, "Your account has been created")
            return redirect("jobs")
        else:
            messages.error(request, "Registration failed")
            context = {
                "company_form": company_form,
                "company_user_form": company_user_form
            }
            return render(request, "company/company_registration.html", context)


class LogInView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,"company/login.html",context={"form":form})

    def post(self,request,*args,**kwargs):
        form =LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request,email=email, password=password)
            if user is not None:
                if user.role == 1:
                    login(request, user)
                    return redirect('company-dashboard')
            else:
                print("failure")
                return render(request,"company/login.html",context={"form":form})
        return render(request,"registration.html")


class CompanyDashboardView(View):
    def get(self, request):
        return render(request, 'company/company-dashboard.html')
