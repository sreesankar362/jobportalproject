from datetime import date

from django.views.generic import View,FormView,DetailView,TemplateView
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import JobModel
from .forms import JobModelForm,JobSearchForm
from django.contrib import messages
from subscription.models import CompanySubscription
from companyaccount.models import CompanyProfile


class HomeView(TemplateView):
    template_name = "home/home.html"


class JobListingView(TemplateView):
    template_name = "home/job_listing.html"

    def get(self,request):
        search_form = JobSearchForm
        all_jobs = JobModel.objects.filter().order_by("-published_date")
        context = {
            "all_jobs": all_jobs,
            "form": search_form
        }
        return render(request, "home/job_listing.html", context)


def search(request):
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


class JobModelView(FormView):
    template_name = 'post_job.html'
    form_class = JobModelForm

    def get(self, request, *args, **kwargs):
        company = request.user.user
        company_sub = CompanySubscription.objects.filter(company=company)
        is_subscribed = company_sub.filter(end_date__gt=date.today()).exists()
        if is_subscribed and company.is_approved :
            return render(request, self.template_name, {'form': self.form_class()})
        else:
            if not company.is_approved:
                messages.error(request, "Complete Profile and Wait for JobHub's Company Approval to Post Jobs ")
            elif not is_subscribed:
                messages.error(request, "Subscribe JOBHUB to Post Jobs ")
            return redirect('company-dash')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            Job = form.save(commit=False)
            Job.company = request.user.user
            Job.save()
        print("success")
        messages.success(request, "Job Posted Successfully")
        return redirect('company-dash')


class JobDetailView(DetailView): #bibin
    model = JobModel
    context_object_name = "job"
    template_name = "home/job_detail.html"


class AboutUsView(TemplateView):
    template_name = "about_us.html"
