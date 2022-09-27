from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import View
from .forms import CompanyProfileForm, PasswordResetForm, LoginForm
from .models import Company
from django.views.generic import CreateView, FormView, RedirectView,DetailView, UpdateView,TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth


class CreateCompanyProfileView(CreateView):
    
    model_user = Company
    template_name = 'profile/profile-update.html'
    form_class = CompanyProfileForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Company profile has been created.")
        self.object = form.save()
        return super().form_valid(form)


class CompanyProfileUpdateView(UpdateView):
    
    model = Company
    form_class = CompanyProfileForm
    template_name = 'profile/profile-update.html'
    success_url = reverse_lazy("home")
    pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        messages.success(self.request, "Your Company Profile has been successfully updated.")
        self.object = form.save()
        return  super().form_valid(form)


class PasswordResetView(FormView):
    template_name = 'profile/passwordreset.html'
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
                    return redirect("login")
            else:
                messages.error(request, 'invalid credentials')
                return render(request, self.template_name, {'form':form})
            
                        
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

class LoginView(FormView):

    success_url = '/'
    form_class = LoginForm
    template_name = 'profile/login.html'

    # extra_context = {
    #     'title': 'Login'
    # }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    
    
class CompanyProfileView(TemplateView):
    template_name = 'profile/company-profile.html'
    
# class logout_confirm(TemplateView):
#     template_name = 'profile/logout-conformation.html'

def logout_company(request):
    auth.logout(request)
    return redirect('login')
        
        




