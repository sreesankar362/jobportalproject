from django.db import models
from apps.companyaccount.models import CompanyProfile
from datetime import date
import uuid


class Membership(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    membership_days = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.membership_days)


class Payment(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    payment_number = models.UUIDField(default=uuid.uuid4, max_length=200, null=True, blank=True)
    amount_paid = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payment_id)


class CompanySubscription(models.Model):
    company = models.ForeignKey(CompanyProfile, related_name='company_subscription', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    def is_expired(self):
        return self.end_date < date.today()
