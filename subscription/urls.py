from django.urls import path,include
from .views import *

urlpatterns = [
    path('choose', Subscription.as_view(), name="subscription"),
    path('create-checkout-session/', create_checkout_session, name='checkout'),
    # path('payment/<int:mem_id>', PaymentView.as_view(), name="payment"),
    path('payment/success/', success, name="success"),
    path('payment/failed/', PaymentFailed.as_view(), name="failed"),
    path('payment/history', PaymentHistory.as_view(), name="history"),

    ]
