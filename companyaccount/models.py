from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.

class SocialProfile(models.Model):
    website = models.URLField(default="", null=True)
    fb = models.URLField(default="", null=True)
    instagram = models.URLField(default="", null=True)
    linkedin = models.URLField(default="", null=True)

class Company(models.Model):
    users = models.ManyToManyField(User)
    company_name = models.CharField(max_length=100, blank=False)
    company_logo = models.ImageField(
        upload_to="company_images",
        validators= [FileExtensionValidator(allowed_extensions=["jpg","png","jpeg"])],
        null=True
    )
    company_description = models.CharField(max_length=500, null=True)
    company_email = models.EmailField(unique=True,blank=False)
    is_mail_verified = models.BooleanField(default=False)
    phone = models.PositiveIntegerField(null=True)
    location = models.CharField(max_length=100, null=True)
    industry = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    choice = (
        ("0-100","0-100"),
        ("100-500","100-500"),
        ("500-1000","500-1000"),
        ("1000+","1000+")
    )
    team_size = models.CharField(max_length=10, choices=choice, null=True)
    founded = models.PositiveIntegerField(null=True)
    company_address = models.CharField(max_length=250, null=True)
    country_code = models.PositiveIntegerField(null=True)
    social_profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.company_name
