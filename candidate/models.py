from dataclasses import fields
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from autoslug import AutoSlugField
from django_countries.fields import CountryField
from home.models import JobModel
from django.utils import timezone
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date



class LatEducation(models.Model):
    qual_name =  models.CharField(max_length=255, null=True, blank=True)
    qual_institute = models.CharField(max_length=50, null=True, blank=True)
    qual_university = models.CharField(max_length=50, null=True, blank=True)
    percent = models.IntegerField(validators=[MinValueValidator(25),
                                       MaxValueValidator(100)])
    qual_country = country = CountryField(null=True, blank=True)
    
    
class CandidateProfile(models.Model):
    
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    dob = models.DateField(max_length=8)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    latest_edu = models.ForeignKey(LatEducation, on_delete=models.CASCADE, 
                                   null=True, blank=True)
    grad_year = models.IntegerField(blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    slug = AutoSlugField(populate_from='user', unique=True)
    
    def get_absolute_url(self):
        return "/profile/{}".format(self.slug)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    skill = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, related_name='skills', on_delete=models.CASCADE)


class SavedJobs(models.Model):
    job = models.ForeignKey(
        JobModel, related_name='saved_job', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='saved', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job.position


class AppliedJobs(models.Model):
    job = models.ForeignKey(
        JobModel, related_name='applied_job', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='applied_user', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job.position
    


    