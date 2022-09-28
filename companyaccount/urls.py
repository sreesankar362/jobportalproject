from django.urls import path
from companyaccount import views

urlpatterns = [
    path("register",views.CompanyRegistrationView.as_view(),name="register"),
]