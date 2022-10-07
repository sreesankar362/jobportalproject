from django.urls import path,include
from .views import *

urlpatterns = [
    path('choose', Subscription.as_view(), name="subscription"),
    path('payment/<int:mem_id>', PaymentView.as_view(), name="payment"),
    path('payment/status/<int:mem_id>', PaymentView.as_view(), name="status"),

    ]
