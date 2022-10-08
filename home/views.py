from home.forms import JobSearchForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import View, FormView, DetailView
from home.models import JobModel
from .forms import JobModelForm
from django.contrib import messages
from subscription.models import CompanySubscription
from companyaccount.models import CompanyProfile


class HomeView(View):
    def get(self,request):
        return render(request,"home/home.html")


class JobListingView(View):
    def get(self,request):
        search_form = JobSearchForm
        if request.user.is_authenticated:
            sc_sub = CompanySubscription.objects.filter(company=request.user.user)
            is_subscribed = True if True in (sub.is_active(sub) for sub in sc_sub) else False
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

            Job=form.save(commit=False)
            Job.company=request.user.user
            Job.save()

        context = {
            'form':form
        }
        print("success")
        messages.success(request,"Job Posted Successfully")
        return render(request,"company/company-dashboard.html", {'form': form})


class JobDetailView(DetailView): #bibin
    model = JobModel
    context_object_name = "job"
    template_name = "home/job_detail.html"
