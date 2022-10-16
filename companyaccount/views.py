from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str

from home.models import JobModel
from .token import account_activation_token
from .utils import company_activation_mail
from subscription.models import CompanySubscription
from django.views.generic import View
from companyaccount.forms import CompanyRegistrationForm
from user.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib import messages
from accounts.models import User
from django.views.generic import CreateView, FormView, UpdateView, TemplateView
from django.urls import reverse_lazy
from accounts.verified_access import login_company_required
from django.utils.decorators import method_decorator
from datetime import date
import datetime
from candidate.models import JobApplication

from django.core.mail import send_mail
from django.conf import settings


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
            company_activation_mail(request, user_obj, company_user_form)
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
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        company = CompanyProfile.objects.get(user=user)
        company.is_activated = True
        company.is_mail_verified = True
        company.save()
        messages.info(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('company-login')
    else:
        messages.error(request, 'Token Expired.')
        return redirect('company-login')


class LogInView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "company/login.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.role == 1:
                    login(request, user)
                    messages.info(request, "Your are logged in")
                    return redirect('company-dash')
                else:
                    messages.info(request, "Credentials did not match with Company account")
                    return redirect("login")
            else:

                try:
                    company = CompanyProfile.objects.get(user=User.objects.get(email=email))
                    if not company.is_activated:
                        messages.info(request, "Activate your account via mail to login")
                finally:
                    messages.error(request, "Invalid Credentials")
                    return render(request, "company/login.html", context={"form": form})

        return render(request, "registration.html")


@method_decorator(login_company_required, name="dispatch")
class CompanyDashboardView(View):
    def get(self, request):
        active_sub = None
        remaining = 0
        company = request.user.user
        print(company)

        sub = CompanySubscription.objects.filter(company=company)
        if sub.filter(end_date__gt=date.today()).exists():
            active_sub = sub.get(end_date__gt=date.today())
            remaining = active_sub.end_date - active_sub.start_date
        context = {
            "company": company,
            "active_sub": active_sub,
            "remaining": remaining
        }
        return render(request, 'company/company-dashboard.html', context)


@method_decorator(login_company_required, name="dispatch")
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


@method_decorator(login_company_required, name="dispatch")
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


@method_decorator(login_company_required, name="dispatch")
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


@method_decorator(login_company_required, name="dispatch")
class CompanyProfileView(TemplateView):
    template_name = 'company/company-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company_data"] = CompanyProfile.objects.filter(user=self.request.user)
        return context


class ApplicationsView(View):
    def get(self, request):
        company = request.user.user
        company_sub = CompanySubscription.objects.filter(company=company)
        is_subscribed = company_sub.filter(end_date__gt=date.today()).exists()
        if is_subscribed and company.is_approved:
            applications = JobApplication.objects.filter(company=request.user.user).order_by("-applied_date")
            context = {
                "applications": applications
            }
            return render(request, 'company/applications.html', context)
        else:
            if not company.is_approved:
                messages.error(request, "Company Profile not Approved ")
            elif not is_subscribed:
                messages.error(request, "Subscribe JOBHUB to View Applications ")
            return redirect('company-dash')


def accept_job(request, **kwargs):
    app_id = kwargs.get("appl_id")
    application = JobApplication.objects.get(id=app_id)
    application.job_status = 'accepted'
    application.processed_date = date.today()
    application.save()
    # sendmail
    recipient = application.candidate.user.email
    print(recipient)
    send_mail(
        'Congrats! We have accepted your job application.',
        "Luckily, your profile seems to match our requirements."
        "We are forwarding your application because we found your profile quite impressive."
        "We thankyou for choosing us to find a right job for you.\n"
        'Thanks and Regards,\n'
        'Team JOBHUB',
        settings.EMAIL_HOST_USER,
        [recipient],
        fail_silently=False
    )
    print(application.job_status)
    return redirect("apps")


def reject_job(request, **kwargs):
    app_id = kwargs.get("appl_id")
    application = JobApplication.objects.get(id=app_id)
    application.job_status = 'rejected'
    application.processed_date = date.today()
    print(date.today())
    application.save()
    # sendmail
    recipient = application.candidate.user.email
    print(recipient)
    send_mail(
        'Sorry! We have rejected your job application.',
        "Unfortunately, your profile doesn't match our requirements."
        "We would not be able to take this forward."
        "We urge you to keep a tab on our page and apply for future job openings.\n"
        'Thanks and Regards,\n' 
        'Team JOBHUB',
        settings.EMAIL_HOST_USER,
        [recipient],
        fail_silently=False
    )
    print(application.job_status)
    return redirect("apps")


def delete_application(request, **kwargs):
    app_id = kwargs.get("appl_id")
    application = JobApplication.objects.get(id=app_id)
    application.delete()
    print(application.job_status)
    return redirect("apps")
