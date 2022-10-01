
from django.urls import path
from companyaccount import views

urlpatterns = [
    path("register", views.CompanyRegistrationView.as_view(), name="company-register"),
    path("login", views.LogInView.as_view(), name="company-login"),
    path("dashboard", views.CompanyDashboardView.as_view(), name="company-dashboard"),

]
