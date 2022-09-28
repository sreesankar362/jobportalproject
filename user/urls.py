from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from user import views as userviews
urlpatterns=[

    path("register", userviews.RegistrationView.as_view(), name="register"),
    path("login", userviews.LogInView.as_view(), name="login"),
    path("logout", userviews.LogOutView.as_view(), name="logout"),
    path("welcome", userviews.WelcomeView.as_view(), name="welcome")

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)