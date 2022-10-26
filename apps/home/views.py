from datetime import date
from django.views.generic import FormView, TemplateView, View
from django.db.models import Q
from django.shortcuts import render, redirect
from apps.candidate.models import SavedJobs, JobApplication
from .models import JobModel
from .forms import JobModelForm, EnquiryForm
from django.contrib import messages
from apps.subscription.models import CompanySubscription
from apps.accounts.verified_access import login_company_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from .filters import JobListingFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def handler400(request, exception):
    return render(request, 'error_handler/error_400.html', status=400)


def handler403(request, exception):
    return render(request, 'error_handler/error_403.html', status=403)


def handler404(request, exception):
    return render(request, 'error_handler/error_404.html', status=404)


def handler500(request):
    return render(request, 'error_handler/error_500.html', status=500)


class HomeView(TemplateView):
    """
    Displays the homepage.

    Takes job model objects and slicing latest 5 jobs to list as recent jobs.
    """
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_jobs"] = JobModel.objects.all().order_by("-published_date").filter(is_active=True)[:5]
        return context


def inactive_job(request, *args, **kwargs):
    """
    this function tells if a job posted by the recruiter is active or not when clicked on the 'Active'button
    in the 'Posted Jobs' tab
    True indicates the job is active,
    False indicates the job got expired

    this function can change the status of the job and returns a message indicating so.
    """
    job_id = kwargs.get("job_id")
    job = JobModel.objects.get(id=job_id)
    if job.is_active:
        job.is_active = False
        job.save()
        messages.success(request, "job status changed")
        return redirect("postedjob")
    else:
        job.is_active = True
        job.save()
        messages.success(request, "job status changed")
        return redirect("postedjob")


class JobListingView(TemplateView):
    """
    Listing all Jobs.
    All jobs are listed here in their posted date order(latest comes first).
    This view checks if the listing job is in the candidates saved jobs list
    and displays the filter for searching and filtering jobs.
    """
    template_name = "home/job_listing.html"

    def get(self, request):
        all_jobs = JobModel.objects.filter().order_by("-published_date").filter(is_active=True)
        joblistingfilter = JobListingFilter(request.GET, queryset=all_jobs)

        paginator = Paginator(joblistingfilter.qs, 6)
        page = request.GET.get('page')
        paged_jobs = paginator.get_page(page)
        saved_jobs = None
        try:
            if request.user.profile:
                saved_job_obj = SavedJobs.objects.filter(candidate=self.request.user.profile)
                saved_jobs = []
                for sj in saved_job_obj:
                    saved_jobs.append(sj.job)
        except :
            pass
        context = {

            'joblistingfilter': joblistingfilter,
            "all_jobs": paged_jobs,
            "saved_jobs": saved_jobs,
        }
        return render(request, "home/job_listing.html", context)


def search(request):
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        print("keyword")
        if len(keyword):
            all_jobs = JobModel.objects.order_by('-published_date').filter(
                Q(position__icontains=keyword) | Q(job_description__icontains=keyword))

        else:
            return redirect("jobs")

    context = {
        'all_jobs': all_jobs,
    }
    return render(request, "home/job_listing.html", context)


@method_decorator(login_company_required, name="dispatch")
class JobModelView(FormView):
    """
    This class enables the company to post a job after the company approval and successful subscription on
    clicking the 'Post Job' tab

    in case any one of the condition is not satisfied company will be redirected to the dashboard
    on successful post application a success message will be rendered.
    """
    template_name = 'post_job.html'
    form_class = JobModelForm

    def get(self, request, *args, **kwargs):
        company = request.user.user
        company_sub = CompanySubscription.objects.filter(company=company)
        is_subscribed = company_sub.filter(end_date__gt=date.today()).exists()
        if is_subscribed and company.is_approved:
            return render(request, self.template_name, {'form': self.form_class()})
        else:
            if not company.is_approved:
                messages.error(request, "Complete Profile and Wait for JobHub's Company Approval to Post Jobs ")
            elif not is_subscribed:
                messages.error(request, "Subscribe JOBHUB to Post Jobs ")
            return redirect('company-dash')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.user
            job.save()
            messages.success(request, "Job Posted Successfully")
            return redirect('company-dash')
        else:
            messages.error(request, "Job Not posted")
            return render(request, "post_job.html", {'form': form})


class JobDetailView(TemplateView):
    """
    User can view the details of a particular job.
    All the applied jobs are collected in a list and taken as context.
    Returns a template with job details.
    """
    template_name = "home/job_detail.html"

    def get(self, request, *args, **kwargs):
        job_id = kwargs.get("pk")
        print(job_id)
        job = JobModel.objects.get(id=job_id)
        applied_job = None
        if request.user.is_authenticated:
            applied_job_obj = JobApplication.objects.filter(job=job)
            applied_job = []
            for aj in applied_job_obj:
                applied_job.append(aj.job)
        context = {
            "job": job,
            "applied_job": applied_job,
        }
        return render(request, "home/job_detail.html", context)


class AboutUsView(TemplateView):
    template_name = "home/about_us.html"


class EnquiryView(FormView):
    """
    To contact jobhub team if user has any query.
    Renders an enquiry template where query message and details can be added.
    Sends mail with query details to jobhub's email and redirects to home page.
    """
    template_name = 'home/enquiry.html'
    form_class = EnquiryForm

    def post(self, request, *args, **kwargs):
        form = EnquiryForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            form.save()

            send_mail(
                "Enquiry for JOBHUB",
                f"Name: {first_name} {last_name}, Email address: {email}, Message: {message}",
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
            messages.success(request, "Enquiry sent")
            return redirect("home")
        else:
            messages.error(request, "Failed to sent enquiry")
            return render(request, "home/enquiry.html", {"form": form})


class JobPostView(View):
    def get(self, request, *args, **kwargs):
        """
        This class lists all the jobs posted by the recruiter when clicked on 'Posted Jobs' tab

        renders a html page that lists all the jobs posted by the recruiter
        """
        if request.user.is_authenticated:
            jobs = JobModel.objects.filter(company=request.user.user).order_by('-published_date')
            context = {
                "jobs": jobs,
            }
            return render(request, "company/posted_job.html", context)
