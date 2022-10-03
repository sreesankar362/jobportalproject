from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class ApplicantUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
   # is_mail_verified = models.BooleanField(default=False)
    dob = models.CharField(max_length=15)
    mobile = models.CharField(max_length=20)
    #is_phone_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='images',null=True,blank=True)
    options = (
        ("male", "Male"),
        ("Female", "Female"),
        ("Others", "Others")
    )
    gender = models.CharField(max_length=10,choices=options)
    bio = models.TextField(max_length=500)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        full_name = (self.first_name,self.last_name)
        return full_name.strip()
