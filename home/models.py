from django.db import models
from companyaccount.models import CompanyProfile
from accounts.models import User


class JobModel(models.Model):
    position = models.CharField(max_length=100)
    job_description = models.TextField(max_length=800)
    skills = models.TextField(max_length=200)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='employer')
    job_type = (
        ("Full Time", "full time"),
        ("Part Time", 'Part Time'),
        ("Temporary", 'Temporary'),
        ("Contract", 'Contract'),
        ("Freelance", 'Freelance')
    )
    job_type = models.CharField(max_length=50, choices=job_type)
    published_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    application_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    min_experience = models.PositiveIntegerField(null=True, blank=True)
    max_experience = models.PositiveIntegerField(null=True, blank=True)
    min_salary = models.IntegerField(null=True, blank=True)
    max_salary = models.IntegerField(null=True, blank=True)
    No_of_openings = models.IntegerField(null=True, blank=True)
    min_qualification = models.CharField(max_length=100, null=True, blank=True)
    categories = models.CharField(max_length=100)
    work_type = (
        ("Work From Home", "Work from Home"),
        ("Work From Office", "Work from Office"),
        ("Hybrid", "Hybrid")
    )
    work_type = models.CharField(max_length=50, choices=work_type)

    def __str__(self):
        return self.position

class Enquiry(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.CharField(max_length=200)

    def __str__(self):
        return self.email


