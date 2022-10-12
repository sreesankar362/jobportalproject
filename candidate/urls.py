from django.urls import path
from .views import AddCandidateView, ViewCandidateView, CandidateProfileUpdateView, apply_job
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("add_candidate", AddCandidateView.as_view(), name="add_candidate"),
    path("viewcandidate/<str:slug>", ViewCandidateView.as_view(), name="view_candidate"),
    path('profile_update/<str:slug>', CandidateProfileUpdateView.as_view(), name='profile_update'),
    path('apply_job/<int:job_id>/<str:slug>', apply_job, name='apply_job'),
    # path('apply_job/<int:job_id>', apply_job, name='apply_job'),
]
