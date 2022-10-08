from django.db import models
from companyaccount.models import CompanyProfile
import uuid
from datetime import date, timedelta

MEM_TYPE = (
    ('Free', 'free'),
    ('Paid', 'paid')
)


class Membership(models.Model):
    membership_days = models.IntegerField(default=7)
    price = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=20, choices=MEM_TYPE, default='paid')

    def __str__(self):
        return str(self.membership_days)


class Payment(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False)
    amount_paid = models.CharField(max_length=100)
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

    def is_active(self, obj):
        return date.today() < obj.end_date
