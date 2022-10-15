from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from .forms import CandidateProfileForm, LatEducationForm, ExperienceForm
from accounts.models import User
from accounts.verified_access import login_required  # decorator
from django.utils.decorators import method_decorator
from .models import CandidateProfile, SavedJobs, Experience, JobModel, JobApplication


@method_decorator(login_required, name="dispatch")
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


def save_job(request, *args, **kwargs):
    try:
        if request.user.is_authenticated and request.user.profile:
            candidate = request.user.profile
            job_id = kwargs.get("job_id")
            job = JobModel.objects.get(id=job_id)
            job = SavedJobs(candidate=candidate, job=job)
            job.save()
            messages.success(request, "saved")
            return redirect("jobs")
        else:
            messages.error(request, "Login To Save Job")
            return redirect("jobs")
    except:
        messages.error(request,"Sorry Recruiters Cannot Save Jobs")
        return redirect("jobs")


def unsave_job(request, *args, **kwargs):
    candidate = request.user.profile
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    saved_job = SavedJobs.objects.filter(candidate=candidate, job=job)
    saved_job.delete()
    messages.success(request, "unsaved")

    return redirect("jobs")


class SavedJobsView(TemplateView):
    template_name = 'jobseeker/saved_jobs.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SavedJobsView, self).get_context_data(*args, **kwargs)
        savedjobsobjects = SavedJobs.objects.filter(candidate=self.request.user.profile)

        for savedjob in savedjobsobjects:
            print(savedjob.job.job_description)

        context['savedjobsobjects'] = savedjobsobjects
        return context


class ViewCandidateView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        can = CandidateProfile.objects.get(slug=slug)
        exp = Experience.objects.filter(candidate=request.user.profile)
        context = {
            "can": can,
            "exp": exp,
        }
        return render(request, "jobseeker/candidate-profile.html", context)


class CandidateProfileUpdateView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        profile = CandidateProfile.objects.get(slug=slug)
        form = CandidateProfileForm(instance=profile)
        return render(request, "jobseeker/update_profile.html", {"form": form})

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        profile = CandidateProfile.objects.get(slug=slug)
        form = CandidateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Candidate Profile has been updated")
            return redirect("myaccount")
        else:
            messages.error(request, "Error in updating")
            return render(request, "jobseeker/profile_update.html", {"form": form})


def apply_job(request, *args, **kwargs):
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    slug = kwargs.get("slug")
    candidate = CandidateProfile.objects.get(slug=slug)
    JobApplication.objects.create(job=job, candidate=candidate)
    messages.success(request, 'Successfully applied for the job')
    return redirect('jobs')


class JobApplicationView(TemplateView):
    template_name = 'jobseeker/applied_jobs.html'

    def get_context_data(self, *args, **kwargs):
        context = super(JobApplicationView, self).get_context_data(*args, **kwargs)
        jobapplicationobjects = JobApplication.objects.filter(candidate=self.request.user.profile)
        print(jobapplicationobjects)
        for objects in jobapplicationobjects:
            print(objects.job.position)
        context['jobapplicationobjects'] = jobapplicationobjects

        return context
