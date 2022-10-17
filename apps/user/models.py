# from django.db import models
# from accounts.models import User
#
#
# class ApplicantUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     dob = models.CharField(max_length=15)
#     options = (
#         ("male", "Male"),
#         ("Female", "Female"),
#         ("Others", "Others")
#     )
#     gender = models.CharField(max_length=10, choices=options)
#
#     def __str__(self):
#         return self.user.username
#
#     def get_full_name(self):
#         full_name = (self.first_name,self.last_name)
#         return full_name.strip()
