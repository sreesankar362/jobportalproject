from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, JobListingView,JobModelView, search, JobDetailView


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('jobs', JobListingView.as_view(), name="jobs"),
    path('user/', include("user.urls")),
    path('jobs/search', search, name="search"),
    path('postjob', JobModelView.as_view(),name="post_job"),
    path('job_detail/<int:pk>', JobDetailView.as_view(), name="job_detail"),  # bibin
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
