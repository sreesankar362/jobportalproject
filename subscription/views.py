from django.shortcuts import render
from .utils import *
from datetime import date, timedelta
from django.utils import timezone
from django.views.generic import View
from.models import Membership, Payment, CompanySubscription


class Subscription(View):

    def get(self, request, *args, **kwargs):
        mem = Membership.objects.all()
        context = {
            "mem": mem
        }
        return render(request, 'subscription/choose_membership.html', context)


class PaymentView(View):
    def get(self, request, *args, **kwargs):

        start_date = date.today()
        sc_sub = CompanySubscription.objects.filter(company=request.user.user)
        is_subscribed = True if True in (sub.is_active(sub) for sub in sc_sub) else False
        last_date = date.today()
        for sc in sc_sub:
            if sc.end_date > last_date:
                last_date = sc.end_date

        mem_id = kwargs.get("mem_id")
        membership = Membership.objects.get(id=mem_id)
        sub_days = membership.membership_days
        expiry_date = start_date + timedelta(days=sub_days)
        per_month = (membership.price/sub_days)*30
        context = {
            "membership": membership,
            "start_date": start_date,
            "expiry_date": expiry_date,
            "per_month": per_month,
            "is_subscribed": is_subscribed,
            "last_date": last_date
        }

        return render(request, 'subscription/payment.html', context)

    def post(self, request, *args, **kwargs):
        mem_id = kwargs.get("mem_id")
        membership = Membership.objects.get(id=mem_id)

        payment = Payment(company=request.user.user, amount_paid=membership.price,
                          status='success')
        payment.save()
        start_date = date.today()
        expiry_date = start_date + timedelta(days=membership.membership_days)
        subscription = CompanySubscription(company=request.user.user,
                                           membership=membership,
                                           start_date=start_date,
                                           end_date=expiry_date,
                                           payment=payment)
        subscription.save()
        context = {
            "payment_id": payment.payment_id,
            "status": payment.status,
            "amount_paid": payment.amount_paid
        }

        return render(request, 'subscription/payment_status.html', context)

