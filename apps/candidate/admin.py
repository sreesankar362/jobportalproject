from django.contrib import admin
from .models import *


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'company', 'applied_date', 'job_status', 'processed_date']


admin.site.register(JobApplication, JobApplicationAdmin)

admin.site.register(CandidateProfile)

admin.site.register(LatEducation)

admin.site.register(Experience)



