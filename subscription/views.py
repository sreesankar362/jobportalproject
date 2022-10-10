from accounts.verified_access import login_company_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from datetime import date, timedelta
from django.views.generic import View, TemplateView
from.models import Membership, Payment, CompanySubscription


@method_decorator(login_company_required,name="dispatch")
class Subscription(TemplateView):
    template_name = "subscription/choose_membership.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Subscription, self).get_context_data(*args, **kwargs)
        context['mem'] = Membership.objects.all()
        return context


@method_decorator(login_company_required,name="dispatch")
class PaymentView(View):
    def get(self, request, *args, **kwargs):
        start_date = date.today()
        company = request.user.user
        company_sub = CompanySubscription.objects.filter(company=company)
        is_subscribed = company_sub.filter(end_date__gt=date.today()).exists()
        last_date = date.today()
        for sub in company_sub:
            if sub.end_date > last_date:
                last_date = sub.end_date
        mem_id = kwargs.get("mem_id")
        membership = Membership.objects.get(id=mem_id)
        sub_days = membership.membership_days
        expiry_date = start_date + timedelta(days=sub_days)
        per_month = (membership.price/sub_days)*30
        context = {
            "company": company,
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
            "payment": payment
        }
        return render(request, 'subscription/payment_status.html', context)


@method_decorator(login_company_required,name="dispatch")
class PaymentHistory(TemplateView):
    template_name = "subscription/payment-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentHistory, self).get_context_data(*args, **kwargs)
        company = self.request.user.user
        context['payments'] = Payment.objects.filter(company=company)
        return context
