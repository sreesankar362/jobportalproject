from django.db import models
from accounts.models import User
from django.core.validators import FileExtensionValidator
from.utils import send_approve_notification


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=False)
    company_logo = models.ImageField(
        upload_to="company_images",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
        null=True,blank=True,
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
    company_address = models.TextField(max_length=250, null=True, blank=True)

    is_activated = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_mail_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = CompanyProfile.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'admin/admin_approval_mail.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved:
                    # Send notification email
                    mail_subject = "Greetings from JobHub! Your Company has been approved."
                    send_approve_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your job openings in JobHub."
                    send_approve_notification(mail_subject, mail_template, context)
        return super(CompanyProfile, self).save(*args, **kwargs)
