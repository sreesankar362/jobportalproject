from django.shortcuts import render,redirect
from django.views.generic import View
from companyaccount.forms import CompanyRegistrationForm,CompanyUserForm
from django.contrib import messages

# Create your views here.

class CompanyRegistrationView(View):
    def get(self, request, *args, **kwargs):
        company_form = CompanyRegistrationForm()
        company_user_form = CompanyUserForm()
        context = {
            "company_form": company_form,
            "company_user_form": company_user_form
        }
        return render(request, "company/company_registration.html", context)

    def post(self, request, *args,**kwargs):
        company_form = CompanyRegistrationForm(request.POST)
        company_user_form = CompanyUserForm(request.POST)
        if company_form.is_valid() and company_user_form.is_valid():
            company_obj = company_form.save()
            user_obj = company_user_form.save()
            company_obj.users.add(user_obj)
            messages.success(request, "Your account has been created")
            return redirect("jobs")
        else:
            messages.error(request, "Registration failed")
            context = {
                "company_form": company_form,
                "company_user_form": company_user_form
            }
            return render(request, "company/company_registration.html", context)



