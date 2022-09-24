from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
# Create your models here.
<<<<<<< Updated upstream
class DemoModel(models.Model):
  print("hello")

class ModelDemo(models.Model):
    print("hi")
    print("seconf hi")

    
class ModelDemosecond(models.Model):
    print("hi")
    print("seconf hi")

class ModelDemoThird(models.Model):
    print("hi")
    print("seconf hi")
=======


class ApplicantUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
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
>>>>>>> Stashed changes
