from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, JobListingView, JobModelView,JobDetailView,AboutUsView, search,JobPostView, EnquiryView


urlpatterns = [
                  path('', HomeView.as_view(), name="home"),
                  path('jobs', JobListingView.as_view(), name="jobs"),
                  path('about_us', AboutUsView.as_view(), name="about_us"),
                  path('jobs/search', search, name="search"),
                  path('user/', include("apps.user.urls")),
                  path('postjob', JobModelView.as_view(), name="post_job"),
                  path('postedjob', JobPostView.as_view(), name="postedjob"),
                  path('enquiry', EnquiryView.as_view(), name="enquiry"),
                  path('job_detail/<int:pk>', JobDetailView.as_view(), name="job_detail"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

