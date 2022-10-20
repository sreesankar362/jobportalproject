from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .forms import EduFormSet, ExpFormSet, CandidateFormSet
from apps.accounts.verified_access import login_required  # class auth decorator
from .models import CandidateProfile, SavedJobs, Experience, JobModel, JobApplication, LatEducation


@method_decorator(login_required, name="dispatch")
class AddCandidateView(TemplateView):
    """Candidate/Job Seeker Profile is addes once login happens.
    Here all the date taken as formset with prefixes
    and store in db with adding user/instance datas.
    """
    template_name = "jobseeker/add_candidate.html"

    def get(self, *args, **kwargs):
        """Three formsets are transferred to jobseeker/add_candidate.html with unique prefixes"""

        edu_formset = EduFormSet(queryset=LatEducation.objects.none(), prefix="edu")
        exp_formset = ExpFormSet(queryset=Experience.objects.none(), prefix="exp")
        candidate_formset = CandidateFormSet(queryset=CandidateProfile.objects.none(), prefix="candidate")

        return self.render_to_response(
            {'edu_formset': edu_formset, 'exp_formset': exp_formset, "candidate_formset": candidate_formset})

    def post(self, *args, **kwargs):

        """Data received here with unique prefixes,accessed with respective formsets
        and validity of forms checked and saved.
        """
        edu_formset = EduFormSet(self.request.POST, prefix="edu")
        exp_formset = ExpFormSet(self.request.POST, prefix="exp")
        candidate_formset = CandidateFormSet(self.request.POST, self.request.FILES, prefix="candidate")
        print(self.request.POST)  # checking the post data received.

        if edu_formset.is_valid() and exp_formset.is_valid() and candidate_formset.is_valid():
            lat_education_form_obj = edu_formset.save()
            candidate_profile_objs = candidate_formset.save(
                commit=False)  # need to insert some fields before committing
            exp_obj = exp_formset.save(commit=False)
            for profile in candidate_profile_objs:
                profile.user = self.request.user
                for edu in lat_education_form_obj:
                    profile.latest_edu = edu
                    break  # Only first value storing in DB since no user field for 'latest_edu'
                profile.save()
                for exp in exp_obj:
                    exp.candidate = profile  # Here the candidate field holds the full profile.
                    exp.save()

            return redirect(reverse_lazy("myaccount"))
        else:
            print("Form Error")
            messages.error(self.request, "Error in AddCandidateView Form ")

        return self.render_to_response(
            {'edu_formset': edu_formset, 'exp_formset': exp_formset, "candidate_formset": candidate_formset})


def save_job(request, *args, **kwargs):
    """
    This function saves the job once the candidate clicks the save button after successful login, if not will
    be asked to log-in

    returns a successfully saved message
    """
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
    """
    this function unsaves the job when clicked on the unsave button

    returns an unsaved successfully message and displays the save button back
    """
    candidate = request.user.profile
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    saved_job = SavedJobs.objects.filter(candidate=candidate, job=job)
    saved_job.delete()
    messages.success(request, "unsaved")

    return redirect("jobs")


@method_decorator(login_required, name="dispatch")
class SavedJobsView(View):
    def get(self, request, *args, **kwargs):
        """
        This class lists the jobs saved by the candidate in Saved Jobs

        Renders a template that displays all the jobs saved by the candidate if the candidate has created a
        profile else will be asked to complete the profile creation
        """
        try:
            candidate = request.user.profile
            savedjobsobjects = SavedJobs.objects.filter(candidate=candidate)
            if request.user.profile:
                for savedjob in savedjobsobjects:
                    print(savedjob.job.job_description)
                context = {
                    'savedjobsobjects': savedjobsobjects
                }
                return render(request, 'jobseeker/saved_jobs.html', context)
        except:
            messages.error(request, "Please add your profile ")
            return redirect('myaccount')


@method_decorator(login_required, name="dispatch")
class ViewCandidateView(View):
    def get(self, request, *args, **kwargs):
        """
        This Class displays the profile created by the candidate when clicked on 'Profile' tab

        renders a template containing candidate profile details entered by the candidate
        """
        slug = kwargs.get("slug")
        can = CandidateProfile.objects.get(slug=slug)
        exp = Experience.objects.filter(candidate=can)
        context = {
            "can": can,
            "exp": exp,
        }
        return render(request, "jobseeker/candidate-profile.html", context)


@method_decorator(login_required, name="dispatch")
class CandidateProfileUpdateView(TemplateView):
    """
    Candidates can update their profile
    Displays update profile template where they can update neccesary fields
    Returns a success message after updation and redirects to dashboard
    """
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
    """
    Candidate can apply for a job.
    This function creates a job application taking candidate profile & job.
    Displays disabled Applied button after job is applied.
    Returns a success message after job is applied and redirects to job listing page.
    """
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    slug = kwargs.get("slug")
    candidate = CandidateProfile.objects.get(slug=slug)
    JobApplication.objects.create(job=job, candidate=candidate, company=job.company)
    messages.success(request, 'Successfully applied for the job')
    return redirect('jobs')


@method_decorator(login_required, name="dispatch")
class JobApplicationView(View):
    def get(self, request, *args, **kwargs):
        """
        This class lists all the jobs applied by the candidate when clicked on the 'My Applications' tab if the
        candidate has completed the profile creation,else will be asked to add the profile

        renders a template listing all the jobs applied by the candidate
        """
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
