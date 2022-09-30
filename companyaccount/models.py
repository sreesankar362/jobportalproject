from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import FileExtensionValidator

User = get_user_model()

class SocialProfile(models.Model):
    website = models.URLField(default="", null=True)
    fb = models.URLField(default="", null=True)
    instagram = models.URLField(default="", null=True)
    linkedin = models.URLField(default="", null=True)

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=False)
    company_logo = models.ImageField(upload_to="companyimages", validators= [FileExtensionValidator(allowed_extensions=["jpg","png","jpeg"])])
    company_description = models.CharField(max_length=500, null=True)
    industry = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    choice1=(
        ("full-time","full-time"),
        ("part-time","part-time"),
        ("intern","intern")
    )
    type = models.CharField(max_length=100, choices=choice1)
    founded = models.PositiveIntegerField(null=True)
    choice2 = (
        ("0-100","0-100"),
        ("100-500","100-500"),
        ("500-1000","500-1000"),
        ("1000+","1000+")
    )
    team_size = models.CharField(max_length=10, choices=choice2)
    company_email = models.EmailField(unique=True, blank=False, error_messages={"unique":"A user with this email already exist"})
    is_mail_verified = models.BooleanField(default=False)
    phone = models.PositiveIntegerField(null=True)
    location = models.CharField(max_length=100)
    company_address = models.CharField(max_length=250, null=True)
    country_code = models.PositiveIntegerField(null=True)
    social_profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)


