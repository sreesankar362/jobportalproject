from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import CandidateProfileForm, LatEducationForm, ExperienceForm
from accounts.models import User
from accounts.verified_access import login_required #decorator
from django.utils.decorators import method_decorator

from .models import CandidateProfile


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
