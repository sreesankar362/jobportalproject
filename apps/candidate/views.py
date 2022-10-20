from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from .forms import EduFormSet, ExpFormSet, CandidateFormSet
from apps.accounts.verified_access import login_required  # decorator
from django.utils.decorators import method_decorator
from .models import CandidateProfile, SavedJobs, Experience, JobModel, JobApplication,LatEducation
from django.urls import reverse_lazy


@method_decorator(login_required, name="dispatch")
class AddCandidateView(TemplateView):
    template_name = "jobseeker/add_candidate.html"

    def get(self, *args, **kwargs):

        edu_formset = EduFormSet(queryset=LatEducation.objects.none(), prefix="edu")
        exp_formset = ExpFormSet(queryset=Experience.objects.none(), prefix="exp")
        candidate_formset = CandidateFormSet(queryset=CandidateProfile.objects.none(), prefix="candidate")

        return self.render_to_response(
            {'edu_formset': edu_formset, 'exp_formset': exp_formset, "candidate_formset": candidate_formset})

    def post(self, *args, **kwargs):
        edu_formset = EduFormSet(self.request.POST, prefix="edu")
        exp_formset = ExpFormSet(self.request.POST, prefix="exp")
        candidate_formset = CandidateFormSet(self.request.POST, self.request.FILES, prefix="candidate")
        # check post values reach back
        print(self.request.POST)

        if edu_formset.is_valid() and exp_formset.is_valid() and candidate_formset.is_valid():
            print("***********************")
            print(edu_formset)
            print("&&&&&&&&&&&&&&&&&.........")
            print(exp_formset)

            lat_education_form_obj = edu_formset.save()
            candidate_profile_objs = candidate_formset.save(commit=False)
            exp_obj = exp_formset.save(commit=False)

            for profile in candidate_profile_objs:
                profile.user = self.request.user
                for edu in lat_education_form_obj:
                    profile.latest_edu = edu
                    break # Only first value storing in DB
                profile.save()
                for exp in exp_obj:
                    exp.candidate = profile
                    exp.save()

            return redirect(reverse_lazy("myaccount"))
        else:
            print("Form Error")

        return self.render_to_response(
            {'edu_formset': edu_formset, 'exp_formset': exp_formset, "candidate_formset": candidate_formset})


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
        messages.error(request, "Sorry Recruiters Cannot Save Jobs")
        return redirect("jobs")


def unsave_job(request, *args, **kwargs):
    candidate = request.user.profile
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    saved_job = SavedJobs.objects.filter(candidate=candidate, job=job)
    saved_job.delete()
    messages.success(request, "unsaved")

    return redirect("jobs")


class SavedJobsView(View):
    def get(self, request, *args, **kwargs):
        try:
            candidate = request.user.profile
            savedjobsobjects = SavedJobs.objects.filter(candidate=candidate)
            if request.user.profile:
                for savedjob in savedjobsobjects:
                    print(savedjob.job.job_description)
                context = {
                    'savedjobsobjects': savedjobsobjects
                }
                return render(request,'jobseeker/saved_jobs.html', context)
        except:
            messages.error(request, "Please add your profile ")
            return redirect('myaccount')


class ViewCandidateView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        can = CandidateProfile.objects.get(slug=slug)
        exp = Experience.objects.filter(candidate=can)
        context = {
            "can": can,
            "exp": exp,
        }
        return render(request, "jobseeker/candidate-profile.html", context)


class CandidateProfileUpdateView(TemplateView):
    template_name = "jobseeker/update_profile.html"

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        candidate_formset = CandidateFormSet(prefix="candidate", queryset=CandidateProfile.objects.filter(slug=slug))
        return self.render_to_response(
            {
                "candidate_formset": candidate_formset
            })

    def post(self, request, *args, **kwargs):
        candidate_formset = CandidateFormSet(self.request.POST, self.request.FILES, prefix="candidate")

        if candidate_formset.is_valid():
            candidate_formset.save()
            messages.success(request, "Your Candidate Profile has been updated")
            return redirect("myaccount")
        else:
            messages.error(request, "Error in updating")
            return self.render_to_response(
                {"candidate_formset": candidate_formset})


def apply_job(request, *args, **kwargs):
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    slug = kwargs.get("slug")
    candidate = CandidateProfile.objects.get(slug=slug)
    JobApplication.objects.create(job=job, candidate=candidate, company=job.company)
    messages.success(request, 'Successfully applied for the job')
    return redirect('jobs')


class JobApplicationView(View):
    def get(self, request, *args, **kwargs):
        try:
            candidate = request.user.profile
            jobapplicationobjects = JobApplication.objects.filter(candidate=candidate)
            if request.user.profile:
                for objects in jobapplicationobjects:
                    print(objects.job.position)
                context = {
                    "jobapplicationobjects": jobapplicationobjects
                }
                return render(request, "jobseeker/applied_jobs.html", context)
        except:
            messages.error(request, "Please add your profile ")
            return redirect('myaccount')
