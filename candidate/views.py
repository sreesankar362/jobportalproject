from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from home.models import JobModel
from .forms import CandidateProfileForm, LatEducationForm, ExperienceForm
from accounts.models import User
from accounts.verified_access import login_required  # decorator
from django.utils.decorators import method_decorator
<<<<<<< HEAD
from .models import CandidateProfile, SavedJobs


@method_decorator(login_required, name="dispatch")
=======

from .models import CandidateProfile


@method_decorator(login_required,name="dispatch")
>>>>>>> main
class AddCandidateView(View):
    def get(self, request, *args, **kwargs):

        candidate_profile_form = CandidateProfileForm()
        lat_education_form = LatEducationForm()
        experience_form = ExperienceForm()
        form = {
            "candidate_profile_form": candidate_profile_form,
            "lat_education_form": lat_education_form,
            "experience_form": experience_form
        }
        return render(request, "jobseeker/add_candidate.html", form)

    def post(self, request, *args, **kwargs):
        candidate_profile_form = CandidateProfileForm(request.POST)
        lat_education_form = LatEducationForm(request.POST)
        experience_form = ExperienceForm(request.POST)
        if candidate_profile_form.is_valid() and lat_education_form.is_valid() and experience_form.is_valid():
            # saving form values
            lat_education_form_obj = lat_education_form.save()
            # creating candidate profile
            candidate_profile_obj = candidate_profile_form.save(commit=False)
            candidate_profile_obj.latest_edu = lat_education_form_obj
            candidate_profile_obj.user = request.user
            candidate_profile_obj.save()
            exp = experience_form.save(commit=False)
            candidate = candidate_profile_obj
            exp.candidate = candidate
            exp.save()
            return redirect('myaccount')

        else:
            print("Error..................................")
            # messages.error(self.request, "Error in Registration")
            return render(request, "home/home.html")


<<<<<<< HEAD
def save_job(request, *args, **kwargs):
    user = request.user
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    job = SavedJobs(user=user,job=job)
    job.save()
    messages.success(request, "saved")
    return redirect("jobs")


def unsave_job(request, *args, **kwargs):
    user = request.user
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    saved_job = SavedJobs.objects.filter(user=user,job=job)
    print(saved_job)
    saved_job.delete()
    messages.success(request, "unsaved")

    return redirect("jobs")


class SavedJobsView(TemplateView):
    template_name = 'jobseeker/saved_jobs.html'

    def get_context_data(self,*args,**kwargs):
        context = super(SavedJobsView,self).get_context_data(**kwargs)
        savedjobsobjects= SavedJobs.objects.filter(user=self.request.user)

        for savedjob in savedjobsobjects:
            print(savedjob.job.job_description)

        context['savedjobsobjects']=savedjobsobjects
        return context


#class ViewCandidateView(View):
#    def get(self,request,*args,**kwargs):
#        slug=kwargs.get("slug")
#        can = CandidateProfile.objects.get(slug=slug)
#        latest_edu = can.latest_edu

#        return render(request,"jobseeker/candidate-profile.html",{"latest_edu":can})
=======
class ViewCandidateView(View):
    def get(self,request, *args, **kwargs):
        slug = kwargs.get("slug")
        can = CandidateProfile.objects.get(slug=slug)
        context = {
            "can": can,
        }
        return render(request, "jobseeker/viewprofile.html", context)
>>>>>>> main
