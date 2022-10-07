from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, JobListingView,JobModelView



urlpatterns = [
    path('', HomeView.as_view(),name="home"),
    path('jobs', JobListingView.as_view(), name="jobs"),
   # path('postjob', JobPostingView.as_view(), name="post_job"),
    path('user/',include("user.urls")),
    path('postjob',JobModelView.as_view(),name="post_job"),
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



