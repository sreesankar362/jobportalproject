from django.urls import path,include
from . import views
from django.contrib import staticfiles
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "companyaccount"

urlpatterns = [
    
    path('accounts/login',views.LoginView.as_view(), name= 'company-login'),
    path('accounts/logout',views.logout_company, name= 'company-logout'),
    path('users/profile/add',views.CreateCompanyProfileView.as_view(), name = 'add-profile'),
    path('users/profile/view',views.CompanyProfileView.as_view(),name = 'view-profile'),
    path('users/password/reset-password',views.PasswordResetView.as_view(), name = 'reset-pass'),
    path('users/profile/update/<int:user_id>',views.CompanyProfileUpdateView.as_view(), name = 'profile-update'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)