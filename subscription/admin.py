from django.contrib import admin
from .models import Membership, Payment, CompanySubscription
# Register your models here.


class MembershipAdmin(admin.ModelAdmin):
    list_display = ['membership_days', 'price', 'description']


admin.site.register(Membership, MembershipAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['company', 'payment_id', 'amount_paid', 'status', 'created_at', 'email']


admin.site.register(Payment, PaymentAdmin)


class CompanySubscriptionAdmin(admin.ModelAdmin):
    list_display = ['company', 'membership', 'start_date', 'end_date', 'is_expired']


admin.site.register(CompanySubscription, CompanySubscriptionAdmin)
