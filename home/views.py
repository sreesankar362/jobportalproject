from django.shortcuts import render
from django.views.generic import View

from home.forms import JobPostForm
from home.models import JobModel


class HomeView(View):
    def get(self,request):
        return render(request,"home/home.html")


class JobListingView(View):
    def get(self,request):
        all_jobs = JobModel.objects.all().order_by("-published_date")
        context = {
            "all_jobs": all_jobs,
        }
        return render(request, "home/job_listing.html", context)


class JobPostingView(View):
    def get(self, request, *args, **kwargs):
        job_form = JobPostForm
        context = {
            "job_form": job_form
        }
        return render(request, "home/post_job.html", context)
