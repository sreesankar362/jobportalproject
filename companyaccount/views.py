from django.shortcuts import render,redirect
from django.views.generic import View
from companyaccount.forms import CompanyRegistrationForm
from user.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from.models import CompanyProfile
from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages
from accounts.models import User


class CompanyRegistrationView(View):
    def get(self, request, *args, **kwargs):
        company_form = CompanyRegistrationForm()
        company_user_form = RegistrationForm()
        form = {
            "company_form": company_form,
            "company_user_form": company_user_form
        }
        return render(request, "company/company_registration.html", form)

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

            subject = 'Welcome to JOBHUB!'
            message = 'Dear User,\n' \
                      'Thank you for joining JOBHUB. Your account has been registered.\n' \
                      'We are excited to have you on board and looking forward to help you.\n' \
                      'Thanks and Regards,\n' \
                      'Team JOBHUB'
            recipient = company_user_form.cleaned_data.get('email')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

            messages.success(request, "Your account has been created")
            return redirect("company-login")
        else:
            messages.error(request, "Invalid credentials")
            form = {
                "company_form": company_form,
                "company_user_form": company_user_form
            }
            return render(request, "company/company_registration.html", form)


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
                    messages.success(request, "Your are logged in")
                    return redirect('company-dashboard')
            else:
                messages.error(request, "Invalid credentials")
                return render(request,"company/login.html",context={"form":form})
        return render(request,"registration.html")


class CompanyDashboardView(View):
    def get(self, request):
        return render(request, 'company/company-dashboard.html')
