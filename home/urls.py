from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from.views import HomeView,JobListingView


urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('user/',include("user.urls")),
    path('jobs',JobListingView.as_view(), name="jobs")

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



