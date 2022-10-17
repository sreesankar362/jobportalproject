from django.db import models
# from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django_countries.fields import CountryField
from apps.home.models import JobModel
from django.utils import timezone
from apps.accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from apps.companyaccount.models import CompanyProfile


class LatEducation(models.Model):

    qualification = models.CharField(max_length=255, null=True, blank=True)
    institute = models.CharField(max_length=50, null=True, blank=True)
    university = models.CharField(max_length=50, null=True, blank=True)
    percent = models.IntegerField(validators=[MinValueValidator(25), MaxValueValidator(100)])
    passed_year = models.IntegerField(blank=True)
    

class CandidateProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    total_exp = models.PositiveSmallIntegerField(null=True, blank=True)
    summary = models.TextField(max_length=500, null=True, blank=True)
    candidate_image = models.ImageField(
        upload_to="candidate_images",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
        null=True, blank=True,
        default='candidate/default_image.jpg'
    )
    dob = models.DateField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    latest_edu = models.ForeignKey(LatEducation, on_delete=models.CASCADE,
                                   null=True, blank=True)
    languages_known = models.CharField(max_length=300, null=True, blank=True)
    skills = models.CharField(max_length=300, null=True, blank=True)
    address = models.TextField(max_length=350, null=True, blank=True)
    country = CountryField(null=True,blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='user', unique=True)

    def get_absolute_url(self):
        return "/profile/{}".format(self.slug)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name


class Experience(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="exp",
                                  null=True, blank=True)
    experience_field = models.CharField(max_length=255, null=True, blank=True)
    job_position = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    experience_describe = models.TextField(max_length=300, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    exp_duration = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.start_date >= datetime.date.today() or self.end_date >= datetime.date.today():
            raise ValidationError("Sorry, The date entered should be before todays date.")
        super().save(*args, **kwargs)

    def get_exp(self):
        self.exp_duration = int(self.start_date.year - self.end_date.year)


class SavedJobs(models.Model):
    job = models.ForeignKey(
        JobModel, related_name='saved_job', on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE,
                                  null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job.position


class JobApplication(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE,
                                  null=True, blank=True)
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, null=True, blank=True)
    job_status = models.CharField(max_length=20, default='applied')
    applied_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    processed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.job)
