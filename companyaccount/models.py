from django.db import models
from accounts.models import User
from django.core.validators import FileExtensionValidator


# Create your models here.

class SocialProfile(models.Model):
    
    website = models.URLField(default="", null=True)
    fb = models.URLField(default="", null=True)
    instagram = models.URLField(default="", null=True)
    linkedin = models.URLField(default="", null=True)

<<<<<<< HEAD
class Company(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    users = models.ManyToManyField(User)
||||||| 1613bdc
class Company(models.Model):
    users = models.ManyToManyField(User)
=======

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
>>>>>>> f41c6a974fcd56f57609f9cfd08ee6b068f9481a
    company_name = models.CharField(max_length=100, blank=False)
    company_logo = models.ImageField(
        upload_to="company_images",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
        null=True
    )
<<<<<<< HEAD
    company_description = models.CharField(max_length=500, null=True)
    company_email = models.EmailField(unique=True,blank=False)
    is_mail_verified = models.BooleanField(default=False)
    phone = models.PositiveIntegerField(null=True)
    location = models.CharField(max_length=100, null=True)
    industry = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    
    choice1=(
        ("full-time","full-time"),
        ("part-time","part-time"),
        ("intern","intern")
    )

    founded = models.PositiveIntegerField(null=True)
    # choice1=(
    #     ("full-time","full-time"),
    #     ("part-time","part-time"),
    #     ("intern","intern")
    #                             )
    # type = models.CharField(max_length=100, choices=choice1)
    choice2 = (

        ("0-100","0-100"),
        ("100-500","100-500"),
        ("500-1000","500-1000"),
        ("1000+","1000+")
||||||| 1613bdc
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
=======
    company_description = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    choice = (
        ("0-100", "0-100"),
        ("100-500", "100-500"),
        ("500-1000", "500-1000"),
        ("1000+", "1000+")
>>>>>>> f41c6a974fcd56f57609f9cfd08ee6b068f9481a
    )
<<<<<<< HEAD
    team_size = models.CharField(max_length=10, choices=choice2, null=True)
    founded = models.PositiveIntegerField(null=True)
    company_address = models.CharField(max_length=250, null=True)
    country_code = models.PositiveIntegerField(null=True)
    social_profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name='social_pro', null=True)
||||||| 1613bdc
    team_size = models.CharField(max_length=10, choices=choice, null=True)
    founded = models.PositiveIntegerField(null=True)
    company_address = models.CharField(max_length=250, null=True)
    country_code = models.PositiveIntegerField(null=True)
    social_profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, null=True)
=======
    team_size = models.CharField(max_length=10, choices=choice, null=True, blank=True)
    founded = models.PositiveIntegerField(null=True, blank=True)
    company_address = models.CharField(max_length=250, null=True, blank=True)
    country_code = models.PositiveIntegerField(null=True, blank=True)
    social_profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, null=True, blank=True)

    is_approved = models.BooleanField(default=False)
>>>>>>> f41c6a974fcd56f57609f9cfd08ee6b068f9481a

    def __str__(self):
        return self.company_name
    
