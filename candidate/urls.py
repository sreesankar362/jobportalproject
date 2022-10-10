from django.urls import path
from .views import AddCandidateView


urlpatterns = [
    path("add_candidate", AddCandidateView.as_view(), name="add_candidate"),
]
