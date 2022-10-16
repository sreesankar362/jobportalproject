import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.verified_access import login_company_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from datetime import date, timedelta
from django.views.generic import TemplateView
from.models import Membership, Payment, CompanySubscription


stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'https://jobhubonline.herokuapp.com'


@method_decorator(login_company_required, name="dispatch")
class Subscription(TemplateView):
    """
    Lists all available subscriptions as cards.

    on card subscribe button click subscription id is passed to javascript function.
    checkout fn is called passing the id to fn
    """
    template_name = "subscription/choose_membership.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Subscription, self).get_context_data(*args, **kwargs)
        company = self.request.user.user
        company_sub = CompanySubscription.objects.filter(company=company)
        is_subscribed = company_sub.filter(end_date__gt=date.today()).exists()
        print("is_subscribed", is_subscribed)
        context['is_subscribed'] = is_subscribed
        context['mem'] = Membership.objects.all()
        return context


@csrf_exempt
def create_checkout_session(request, **kwargs):
    """
    Creating stripe session returning session ID.

    first membership id is loaded from data to get price and details.
    Stripe session is created by passing the price data and success, cancel urls.
    created stripe session ID is returned to js in choose_membership.html.
    """
    data = json.loads(request.body.decode("utf-8"))
    mem_id = data['id']
    print(mem_id)
    mem = Membership.objects.get(id=mem_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
          'price_data': {
            'currency': 'inr',
            'product_data': {
              'name': mem.description,
            },
            'unit_amount': mem.price*100,
          },
          'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/subscribe/payment/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=YOUR_DOMAIN + '/subscribe/payment/failed',
    )
    print(session.id)
    return JsonResponse({'id': session.id})


def success(request, **kwargs):
    """
    Creating company subscription & Payment

    If stripe checkout is successful session id collected via url
    session is retrieved with session ID and payment details are taken to create Payment and Company Subscription.
    Success template with payment details are rendered in html .
    """
    if "session_id" in request.GET:
        session_id = request.GET['session_id']

        session = stripe.checkout.Session.retrieve(session_id)

        amount = session.amount_total/100
        email = session.customer_details["email"]
        name = session.customer_details["name"]

        membership = Membership.objects.get(price=amount)
        payment = Payment(company=request.user.user,
                          payment_id=session.payment_intent,
                          amount_paid=membership.price,
                          status=session.payment_status,
                          email=email)
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
            "payment": payment,
            "session": session,
            "amount": amount,
            "email": email,
            "name": name
        }
        return render(request, 'subscription/payment_success.html', context)
    else:
        return render(request, 'subscription/payment_failed.html')


@method_decorator(login_company_required, name="dispatch")
class PaymentHistory(TemplateView):
    """
    listing Previous payments

    Sorting payments done by the logged in company and listing as table
    """
    template_name = "subscription/payment-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentHistory, self).get_context_data(**kwargs)
        company = self.request.user.user
        context['payments'] = Payment.objects.filter(company=company).order_by("-created_at")
        return context


class PaymentFailed(TemplateView):
    """
    If stripe checkout session is failed rendering payment_failed.html
    """
    template_name = "subscription/payment_failed.html"
