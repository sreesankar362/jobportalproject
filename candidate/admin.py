from django.contrib import admin
from candidate.models import SavedJobs

from candidate.models import CandidateProfile, Experience,JobApplication

# Register your models here.

# admin.site.register(SavedJobs)
admin.site.register(CandidateProfile)
# admin.site.register(Experience)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'company', 'applied_date', 'job_status', 'processed_date']


admin.site.register(JobApplication, JobApplicationAdmin)
