from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.


class ApplicantUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True)
    email = models.EmailField(unique=True,blank=False,error_messages={"unique":"This email already exists. Already a member?"})
    is_mail_verified = models.BooleanField(default=False)
    dob = models.DateField(null=True)
    mobile = models.CharField(max_length=20,null=True)
    is_phone_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to="media",null=True,validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])])

    options = (
        ("male", "Male"),
        ("Female", "Female"),
        ("Others", "Others")
    )
    gender = models.CharField(max_length=10,choices=options)
    bio = models.TextField(max_length=500,blank=True)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        full_name = (self.first_name,self.last_name)
        return full_name.strip()