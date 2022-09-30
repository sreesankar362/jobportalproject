from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.validators import FileExtensionValidator


class ApplicantUser(AbstractBaseUser):
    """
    Create and save an Applicant with the given username,first_name,last_name,email, password,dob,mobile,gender,profile_pic,
    bio,location.
    """
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=120, unique=True)
    USERNAME_FIELD = "username"
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    email = models.EmailField()
    dob = models.DateField()
    mobile = models.CharField(max_length=20)
    # is_phone_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='images',validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])])
    options = (
        ("male", "Male"),
        ("Female", "Female"),
        ("Others", "Others")
    )
    gender = models.CharField(max_length=10, choices=options)
    bio = models.TextField(max_length=500)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = (self.first_name, self.last_name)
        return full_name.strip()
