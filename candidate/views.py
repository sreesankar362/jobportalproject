from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import CandidateProfileForm, LatEducationForm, SkillForm, ExperienceForm
from accounts.verified_access import login_required  # decorator
from django.utils.decorators import method_decorator


@method_decorator(login_required, name="dispatch")
class AddCandidateView(View):
    def get(self, request, *args, **kwargs):

        form = {
            "candidate_profile_form": CandidateProfileForm(),
            "lat_education_form": LatEducationForm(),
            "experience_form": ExperienceForm(),
            "skill_form": SkillForm()
        }
        return render(request, "jobseeker/add_candidate.html", form)

    def post(self, request, *args, **kwargs):
        candidate_profile_form = CandidateProfileForm(request.POST)
        lat_education_form = LatEducationForm(request.POST)
        experience_form = ExperienceForm(request.POST)
        if candidate_profile_form.is_valid() and lat_education_form.is_valid() and experience_form.is_valid():
            # saving form values
            lat_education_form_obj = lat_education_form.save()
            experience_form_obj = experience_form.save()
            # creating candidate profile
            candidate_profile_obj = candidate_profile_form.save(commit=False)
            candidate_profile_obj.latest_edu = lat_education_form_obj
            candidate_profile_obj.experience = experience_form_obj
            candidate_profile_obj.user = request.user
            candidate_profile_obj.save()
            return redirect('myaccount')

        else:
            print(" Form Error...........................")
            # messages.error(self.request, "Error in Registration")
            form = {
                "candidate_profile_form": CandidateProfileForm(),
                "lat_education_form": LatEducationForm(),
                "experience_form": ExperienceForm(),
                "skill_form": SkillForm()
            }

            return render(request, "jobseeker/add_candidate.html", form)
