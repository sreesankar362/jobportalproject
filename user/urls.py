from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from user import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path("register", views.RegistrationView.as_view(), name="userregister"),
    path("login", views.LogInView.as_view(), name="login"),
    path("logout", views.LogOutView.as_view(), name="logout"),
    path("MyAccount", views.MyAccountView.as_view(), name="myaccount"),

    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='jobseeker/password/changepassworduser.html'),
         name="password_change"),
    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='jobseeker/password/password_change_done.html'),
         name="password_change_done"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='jobseeker/password/password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='jobseeker/password/password_reset_done.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='jobseeker/password/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='jobseeker/password/password_reset_complete.html'),
         name="password_reset_complete"),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)