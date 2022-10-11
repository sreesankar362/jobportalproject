from django.urls import path
from .views import AddCandidateView, ViewCandidateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("add_candidate", AddCandidateView.as_view(), name="add_candidate"),
    path("viewcandidate/<str:slug>", ViewCandidateView.as_view(), name="view_candidate"),
]
