from django.urls import path,include
from . import views
from django.contrib import staticfiles
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('login',views.LogInView.as_view(), name= 'company-login'),
    path('dashboard',views.CompanyDashView.as_view(), name= 'company-dash'),
    path('logout',views.logout_company, name= 'company-logout'),
    path('profile/add/',views.CreateCompanyProfileView.as_view(), name = 'add-profile'),
    path('profile/view',views.CompanyProfileView.as_view(),name = 'view-profile'),
    path('reset-password',views.PasswordResetView.as_view(), name = 'reset-pass'),
    path('profile/update/<int:pk>',views.CompanyProfileUpdateView.as_view(), name = 'profile-update'),
    path("register", views.CompanyRegistrationView.as_view(),name="register"),


]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)