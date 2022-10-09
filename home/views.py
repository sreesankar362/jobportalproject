from django.views.generic import View, FormView, DetailView, TemplateView
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import JobModel
from .forms import JobModelForm, JobSearchForm
from django.contrib import messages
from subscription.models import CompanySubscription
from companyaccount.models import CompanyProfile
from accounts.verified_access import login_required,login_company_required #decorator
from django.utils.decorators import method_decorator

class HomeView(View):  # Home Button Click
    def get(self, request):
        return render(request, "home/home.html")

@method_decorator(login_required,name="dispatch")
class JobListingView(View):  # Jobseeker list jobs
    def get(self, request):
        search_form = JobSearchForm
        if request.user.is_authenticated:
            if request.user.role == 1:
                sc_sub = CompanySubscription.objects.filter(company=request.user.user)
                is_subscribed = True if True in (sub.is_active(sub) for sub in sc_sub) else False
        all_jobs = JobModel.objects.filter().order_by("-published_date")
        context = {
            "all_jobs": all_jobs,
            "form": search_form
        }
        return render(request, "home/job_listing.html", context)

@method_decorator(login_required,name="dispatch")
def search(request):  #Job seeker search jobs
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        print("keyword")
        if len(keyword):
            all_jobs = JobModel.objects.order_by('-published_date').filter(
                Q(position__icontains=keyword) | Q(job_description__icontains=keyword))

        else:
            return redirect("jobs")

    context = {
        'all_jobs': all_jobs,
    }
    return render(request, "home/job_listing.html", context)

@method_decorator(login_company_required,name="dispatch")
class JobModelView(FormView):   # Company post job
    template_name = 'post_job.html'
    form_class = JobModelForm

    def get(self, request, *args, **kwargs):
        company = CompanyProfile.objects.all()

        sc_sub = CompanySubscription.objects.filter(company=request.user.user)
        is_subscribed = True if True in (sub.is_active(sub) for sub in sc_sub) else False
        if is_subscribed is True:
            return render(request, self.template_name, {'form': self.form_class()})
        else:
            messages.error(request, "Subscribe JOBHUB to Post Jobs ")
            return render(request, "company/company-dashboard.html", {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            Job = form.save(commit=False)
            Job.company = request.user.user
            Job.save()

        context = {
            'form': form
        }
        print("success")
        messages.success(request, "Job Posted Successfully")
        return render(request, "company/company-dashboard.html", {'form': form})

@method_decorator(login_required,name="dispatch")
class JobDetailView(DetailView):  # Job seeker click view on job
    model = JobModel
    context_object_name = "job"
    template_name = "home/job_detail.html"


class AboutUsView(TemplateView):  # click button About Us
    template_name = "about_us.html"
@method_decorator(login_required,name="dispatch")  # Job seeker apply job
class JobApplyView(TemplateView):
    template_name = "about_us.html"  # need to overwrite
