from django.shortcuts import render,redirect
from django.views.generic import View
from companyaccount.forms import *
from .models import *
from django.views.generic import CreateView, FormView, RedirectView,DetailView, UpdateView,TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.urls import reverse
from multi_form_view import MultiModelFormView
from django.contrib.auth.decorators import login_required
from user.forms import RegistrationForm, LoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password


class CreateCompanyProfileView(CreateView):
    template_name = 'profile/profile-create.html'
    form_class = CompanyProfileMultiForm
    success_url = reverse_lazy('company-dash')    
        
        
        
class CompanyProfileView(TemplateView):
    template_name = 'profile/company-profile.html'


class CompanyProfileUpdateView(UpdateView):
    
    model = CompanyProfile
    form_class = CompanyProfileMultiForm
    template_name = 'profile/profile-create.html'  
    success_url = reverse_lazy('company-dash') 
    pk_url_kwarg = 'user_id'
    # slug_url_kwarg = 'user_id'

    def form_valid(self, form):
        messages.success(self.request, "Your Company Profile has been successfully updated.")
        self.object = form.save()
        return  super().form_valid(form)


class PasswordResetView(FormView):
    template_name = 'company-password-reset.html'
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data.get('old_password')
            password1 = form.cleaned_data.get('new_password')
            password2 = form.cleaned_data.get('confirm_password')
            user = authenticate(request, username= request.user.username, password = oldpassword)
            if user:
                
                if password1 != password2:
                    messages.error(request, "Passwords Doesn't Match")
                    return redirect('reset-pass')
                else:
                    user.set_password(password2)
                    user.save()
                    messages.success(request, 'Password Changed')
                    return redirect("company-login")
            else:
                messages.error(request, 'invalid credentials')
                return render(request, self.template_name, {'form':form})
            




class LogInView(FormView):

    form_class = LoginForm
    template_name = 'profile/login.html'
    model = CompanyProfile
    def get(self,request,*args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs ):
        form = self. form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user:
                print('success')
                login(request,user)
                return redirect('company-dash')
            else:
                return render(request, self.template_name, {'form':form})

        print(request.POST.get("u_name"))
        print(request.POST.get("pwd"))
        return render(request, 'profile/login.html')


def logout_company(request):
    auth.logout(request)
    return redirect('home')
        
        
class CompanyDashView(TemplateView):
    template_name = 'profile/company-dashboard.html'
    
    
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




















































    
# class LoginView(FormView):

#     form_class = LoginForm
#     template_name = 'profile/login.html'
#     model = User
#     def get(self,request,*args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form':form})

#     def post(self, request, *args, **kwargs ):
#         form = self. form_class(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username = username, password = password)
#             if user:
#                 print('success')
#                 login(request,user)
#                 return redirect('home')
#             else:
#                 return render(request, self.template_name, {'form':form})

#         print(request.POST.get("u_name"))
#         print(request.POST.get("pwd"))
#         return render(request, 'accounts/login.html')

# class LoginView(FormView):

#     success_url = '/'
#     form_class = LoginForm
#     template_name = 'profile/login.html'

#     extra_context = {
#         'title': 'Login'
#     }

#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
#         return super().dispatch(self.request, *args, **kwargs)

#     def get_success_url(self):
#         if 'next' in self.request.GET and self.request.GET['next'] != '':
#             return self.request.GET['next']
#         else:
#             return self.success_url

#     def get_form_class(self):
#         return self.form_class

#     def form_valid(self, form):
#         auth.login(self.request, form.get_user())
#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form):
#         """If the form is invalid, render the invalid form."""
#         return self.render_to_response(self.get_context_data(form=form))

                        

# class LoginView(FormView):

#     form_class = LoginForm
#     template_name = 'profile/login.html'
#     model = User
#     def get(self,request,*args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form':form})
    
    
#     def post(self, request, *args, **kwargs ):
#         form = self. form_class(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username = username, password = password)
#             if user:
#                 print('success')
#                 login(request,user)
#                 return redirect('company-dash')
#             else:
#                 return render(request, self.template_name, {'form':form})

#         print(request.POST.get("u_name"))
#         print(request.POST.get("pwd"))
#         return render(request, 'profile/login.html')



# class LogInView(View):
#     def get(self,request,*args,**kwargs):
#         form = LoginForm()
#         return render(request,"profile/login.html",context={"form":form})

#     def post(self,request,*args,**kwargs):
#         form =LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request,email=email, password=password)
#             if user is not None:
#                 if user.role == 1:
#                     login(request, user)
#                     return render(request, 'profile/company-dashboard.html')
#             else:
#                 print("failure")
#                 return render(request,"profile/login.html",context={"form":form})
#         return render(request,"profile/profile-create.html")


