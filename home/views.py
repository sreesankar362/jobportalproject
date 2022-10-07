from django.shortcuts import render, redirect
from django.views.generic import View

from home.forms import JobSearchForm
from home.models import JobModel

from django.contrib import messages
from django.db.models import Q


class HomeView(View):
    def get(self,request):
        return render(request,"home/home.html")


class JobListingView(View):
    def get(self,request):
        search_form = JobSearchForm
        all_jobs = JobModel.objects.all().order_by("-published_date")
        context = {
            "all_jobs": all_jobs,
            "form": search_form
        }
        return render(request, "home/job_listing.html", context)


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if len(keyword):
            all_jobs = JobModel.objects.order_by('-published_date').filter(
                Q(position__icontains=keyword) | Q(job_description__icontains=keyword))

        else:
            return redirect("jobs")

    context = {
        'all_jobs': all_jobs,
    }
    return render(request, "home/job_listing.html", context)

