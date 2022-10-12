from django.contrib import admin
from candidate.models import CandidateProfile, SavedJobs

from candidate.models import CandidateProfile, Experience

# Register your models here.



admin.site.register(SavedJobs)
admin.site.register(CandidateProfile)
admin.site.register(Experience)

