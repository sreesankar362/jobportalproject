from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import CandidateProfileForm, LatEducationForm, ExperienceForm
from accounts.models import User
from accounts.verified_access import login_required #decorator
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import CandidateProfile, JobApplication, JobModel


@method_decorator(login_required,name="dispatch")
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


class ViewCandidateView(View):
    def get(self,request, *args, **kwargs):
        slug = kwargs.get("slug")
        can = CandidateProfile.objects.get(slug=slug)
        context = {
            "can": can,
        }
        return render(request, "jobseeker/viewprofile.html", context)


class CandidateProfileUpdateView(View):
    def get(self,request,*args,**kwargs):
        slug = kwargs.get("slug")
        profile = CandidateProfile.objects.get(slug=slug)
        form = CandidateProfileForm(instance=profile)
        return render(request,"jobseeker/update_profile.html",{"form":form})

    def post(self,request,*args,**kwargs):
        slug = kwargs.get("slug")
        profile = CandidateProfile.objects.get(slug=slug)
        form = CandidateProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Candidate Profile has been updated")
            return redirect("myaccount")
        else:
            messages.error(request,"Error in updating")
            return render(request,"jobseeker/profile_update.html",{"form":form})


def apply_job(request, *args, **kwargs):
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    slug = kwargs.get("slug")
    candidate = CandidateProfile.objects.get(slug=slug)
    #candidate = CandidateProfile.objects.get(user=request.user)

    JobApplication.objects.create(job=job,candidate=candidate)
    messages.success(request, 'Successfully applied for the job')
    return redirect('jobs')




