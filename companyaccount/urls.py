from django.urls import path
from companyaccount import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register", views.CompanyRegistrationView.as_view(), name="company-register"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("login", views.LogInView.as_view(), name="company-login"),
    path("dashboard", views.CompanyDashboardView.as_view(), name="company-dash"),
    path('profile/add/', views.CreateCompanyProfileView.as_view(), name='add-profile'),
    path('profile/view', views.CompanyProfileView.as_view(), name='view-profile'),
    path('reset-password', views.PasswordResetView.as_view(), name='reset-pass'),
    path('profile/update/<int:user_id>', views.CompanyProfileUpdateView.as_view(), name='profile-update'),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
