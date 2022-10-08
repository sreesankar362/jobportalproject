from django.shortcuts import render
from django.views.generic import View,FormView,DetailView,TemplateView

from home.models import JobModel
from .forms import JobModelForm
from django.contrib import messages

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



class JobModelView(FormView):
    template_name = 'post_job.html'
    form_class = JobModelForm

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

class AboutUsView(TemplateView):
    template_name = "about_us.html"