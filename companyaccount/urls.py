from django.urls import path, include
from .views import CompanyRegisterView

urlpatterns = [
    path('company', CompanyRegisterView.as_view(), name="company")


]


