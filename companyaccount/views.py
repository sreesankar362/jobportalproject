from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

from subscription.models import CompanySubscription
from .token import account_activation_token


from django.views.generic import View
from companyaccount.forms import CompanyRegistrationForm
from user.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages
from accounts.models import User

# nikhils

from django.views.generic import CreateView, FormView, RedirectView,DetailView, UpdateView,TemplateView
from django.urls import reverse_lazy


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
            user_obj.is_active = False
            user_obj.set_password(password)
            user_obj.role = User.EMPLOYER
            user_obj.save()

            company = CompanyProfile(user=user_obj, company_name=company_name)
            company.save()

            current_site = get_current_site(request)
            subject = 'Welcome to JOBHUB!,Verify your Account.'
            message = render_to_string('company/acc_active_email.html', {
                'user': user_obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
                'token': account_activation_token.make_token(user_obj),
            })
            recipient = company_user_form.cleaned_data.get('email')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)

            messages.success(request, "An email has been send to you for account activation.")
            return redirect("company-login")
        else:
            messages.error(request, "Invalid credentials")
            form = {
                "company_form": company_form,
                "company_user_form": company_user_form
            }
            return render(request, "company/company_registration.html", form)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print("try  block")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        print("token check")
        user.save()
        messages.info(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('company-login')
    else:
        pass


class LogInView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,"company/login.html",context={"form":form})

    def post(self,request,*args,**kwargs):
        form =LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.role == 1 and user.is_active:
                    login(request, user)
                    messages.info(request, "Your are logged in")
                    return redirect('company-dash')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Activate your account via mail to login")
                else:
                    messages.error(request, "Invalid credentials/Account not Activated")
                return render(request,"company/login.html",context={"form":form})
        return render(request,"registration.html")


class CompanyDashboardView(View):
    def get(self, request):
        active_sub = None
        print("get")
        sc_sub = CompanySubscription.objects.filter(company=request.user.user)
        for sub in sc_sub:
            if sub.is_active(sub):
                print("active")
                sub_id = sub.id
                active_sub = CompanySubscription.objects.get(id=sub_id)
            else:
                print("else")
                pass

        profile = None
        try:
            profile = CompanyProfile.objects.get(user=request.user)
        except:
            pass
        remaining = 0
        if active_sub:
            print(active_sub.start_date)
            remaining = active_sub.end_date - active_sub.start_date


        context = {
            "profile": profile,
            "active_sub": active_sub,
            "remaining": remaining
        }
        return render(request, 'company/company-dashboard.html', context)


# nikhils addition

class CreateCompanyProfileView(CreateView):
    form_class = CompanyProfileForm
    model = CompanyProfile
    template_name = 'profile/profile-create.html'
    success_url = reverse_lazy('company-dash')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company_name = self.request.user.company_name
        self.object = form.save()
        messages.success(self.request, "Profile Added Successfully!")
        return super().form_valid(form)


class CompanyProfileUpdateView(UpdateView):
    form_class = CompanyProfileForm
    model = CompanyProfile
    template_name = "company/profile-update.html"
    success_url = reverse_lazy('company-dash')
    pk_url_kwarg = 'user_id'
    print("user_id")

    def form_valid(self, form):
        messages.success(self.request, "Your Company Profile has been successfully updated.")
        self.object = form.save()
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = 'company-password-reset.html'
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data.get('old_password')
            password1 = form.cleaned_data.get('new_password')
            password2 = form.cleaned_data.get('confirm_password')
            user = authenticate(request, email=request.user.email, password=oldpassword)
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
                return render(request, self.template_name, {'form': form})


class CompanyProfileView(TemplateView):  # bibin
    template_name = 'company/company-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_data"] = CompanyProfile.objects.filter(user=self.request.user)
        return context
