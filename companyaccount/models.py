from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class SocialProfile(models.Model):
    website = models.URLField(default="", null=True)
    fb = models.URLField(default="", null=True)
    instagram = models.URLField(default="", null=True)
    linkedin = models.URLField(default="", null=True)


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=False)
    company_logo = models.ImageField(
        upload_to="company_images",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
        null=True
    )
    company_description = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    choice = (
        ("0-100", "0-100"),
        ("100-500", "100-500"),
        ("500-1000", "500-1000"),
        ("1000+", "1000+")
    )
    team_size = models.CharField(max_length=10, choices=choice, null=True, blank=True)
    founded = models.PositiveIntegerField(null=True, blank=True)
    company_address = models.CharField(max_length=250, null=True, blank=True)
    country_code = models.PositiveIntegerField(null=True, blank=True)
    social_profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, null=True, blank=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
