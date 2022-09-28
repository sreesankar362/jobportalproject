from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from.forms import CompanyCreationForm,CompanyUserForm
# Create your views here.


class CompanyRegisterView(View):
    def get(self,request):
        company_user_form = UserCreationForm
        company_form = CompanyCreationForm
        context = {
            "company_form" : company_form,
            "user_form" :company_user_form
        }

        return render(request,'register.html',context)

    def post(self,request,*args,**kwargs):
        company_form = CompanyCreationForm(request.POST)
        company_user_form = CompanyUserForm(request.POST)
        if company_form.is_valid() and company_user_form.is_valid() :
            company_obj = company_form.save()
            user_obj = company_user_form.save()
            company_obj.users.add(user_obj)
            return redirect('jobs')
        else:
            print("company_form: ", company_form.errors)
            print("company_user_form: ", company_user_form.errors)
            context = {
                "company_form": company_form,
                "user_form": company_user_form
            }
            return render(request, 'register.html', context)
