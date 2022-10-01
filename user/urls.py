from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from user import views


urlpatterns = [

    path("register", views.RegistrationView.as_view(), name="userregister"),
    path("login", views.LogInView.as_view(), name="login"),
    path("logout", views.LogOutView.as_view(), name="logout"),
    path("MyAccount", views.MyAccountView.as_view(), name="myaccount")

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)