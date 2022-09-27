from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from.views import HomeView


urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('user/',include("user.urls"))

    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



