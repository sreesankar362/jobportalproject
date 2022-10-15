from django.urls import path

from . import views
from .views import AddCandidateView,SavedJobsView,ViewCandidateView, CandidateProfileUpdateView, apply_job


urlpatterns = [
    path("add_candidate", AddCandidateView.as_view(), name="add_candidate"),
    path("viewcandidate/<str:slug>", ViewCandidateView.as_view(), name="view_candidate"),
    path('profile_update/<str:slug>', CandidateProfileUpdateView.as_view(), name='profile_update'),
    path('apply_job/<int:job_id>/<str:slug>', apply_job, name='apply_job'),
    # path('apply_job/<int:job_id>', apply_job, name='apply_job'),
    path("save-jobs/<int:job_id>", views.save_job, name="save-job"),
    path("saved-jobs", SavedJobsView.as_view(), name="saved-job"),
    path("unsave-jobs/<int:job_id>", views.unsave_job, name="unsave-job"),
    path("viewcandidate/<str:slug>",ViewCandidateView.as_view(),name="view_candidate")
]

