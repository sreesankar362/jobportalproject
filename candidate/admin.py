from django.contrib import admin
from candidate.models import CandidateProfile, SavedJobs

# Register your models here.

admin.site.register(CandidateProfile)
admin.site.register(SavedJobs)
