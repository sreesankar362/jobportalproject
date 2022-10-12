from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import AddCandidateView,SavedJobsView,ViewCandidateView


urlpatterns = [
    path("add_candidate", AddCandidateView.as_view(), name="add_candidate"),
    path("save-jobs/<int:job_id>", views.save_job, name="save-job"),
    path("saved-jobs", SavedJobsView.as_view(), name="saved-job"),
    path("unsave-jobs/<int:job_id>", views.unsave_job, name="unsave-job"),
    path("viewcandidate/<str:slug>",ViewCandidateView.as_view(),name="view_candidate")
]

