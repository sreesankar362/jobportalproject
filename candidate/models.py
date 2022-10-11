from django.db import models
from autoslug import AutoSlugField
from django_countries.fields import CountryField
from home.models import JobModel
from django.utils import timezone
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class LatEducation(models.Model):
    qualification = models.CharField(max_length=255, null=True, blank=True)
    institute = models.CharField(max_length=50, null=True, blank=True)
    university = models.CharField(max_length=50, null=True, blank=True)
    percent = models.IntegerField(validators=[MinValueValidator(25), MaxValueValidator(100)])
    passed_year = models.IntegerField(blank=True)
    study_country = CountryField(null=True, blank=True)


class CandidateProfile(models.Model):
    STATE_CHOICES = (

        ("AN", "Andaman and Nicobar Islands"),
        ("AP", "Andhra Pradesh"),
        ("AR", "Arunachal Pradesh"),
        ("AS", "Assam"),
        ("BR", "Bihar"),
        ("CG", "Chhattisgarh"),
        ("CH", "Chandigarh"),
        ("DN", "Dadra and Nagar Haveli"),
        ("DD", "Daman and Diu"),
        ("DL", "Delhi"),
        ("GA", "Goa"),
        ("GJ", "Gujarat"),
        ("HR", "Haryana"),
        ("HP", "Himachal Pradesh"),
        ("JK", "Jammu and Kashmir"),
        ("JH", "Jharkhand"),
        ("KA", "Karnataka"),
        ("KL", "Kerala"),
        ("LA", "Ladakh"),
        ("LD", "Lakshadweep"),
        ("MP", "Madhya Pradesh"),
        ("MH", "Maharashtra"),
        ("MN", "Manipur"),
        ("ML", "Meghalaya"),
        ("MZ", "Mizoram"),
        ("NL", "Nagaland"),
        ("OD", "Odisha"),
        ("PB", "Punjab"),
        ("PY", "Pondicherry"),
        ("RJ", "Rajasthan"),
        ("SK", "Sikkim"),
        ("TN", "Tamil Nadu"),
        ("TS", "Telangana"),
        ("TR", "Tripura"),
        ("UP", "Uttar Pradesh"),
        ("UK", "Uttarakhand"),
        ("WB", "West Bengal")
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    candidate_image = models.ImageField(
        upload_to="candidate_images",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
        null=True, blank=True,
        default='candidate/default_image.jpg'
    )
    dob = models.DateField(max_length=8, null=True, blank=True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    latest_edu = models.ForeignKey(LatEducation, on_delete=models.CASCADE,
                                   null=True, blank=True)
    address = models.TextField(max_length=350, null=True, blank=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=255, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    slug = AutoSlugField(populate_from='user', unique=True)

    # experience = models.ForeignKey(Experience, on_delete=models.CASCADE,
    #                                null=True, blank=True)

    def get_absolute_url(self):
        return "/profile/{}".format(self.slug)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Experience(models.Model):
    experience_field = models.CharField(max_length=255, null=True, blank=True)
    job_position = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    experience_describe = models.TextField(max_length=300, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # end_date = models.DateField(default=datetime.date.today())
    exp_duration = models.IntegerField(default=0)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE,
                                  null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_date >= datetime.date.today() or self.end_date >= datetime.date.today():
            raise ValidationError("Sorry, The date entered should be before todays date.")
        super().save(*args, **kwargs)

    def get_exp(self):
        self.exp_duration = int(self.start_date.year - self.end_date.year)


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


JOB_STATUS = (
    ('Accepted', 'accepted'),
    ('Rejected', 'rejected')
)


class JobApplication(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE,
                                  null=True, blank=True)
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE)
    job_status = models.CharField(choices=JOB_STATUS, max_length=20, default='Applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField()
